import csv
import copy
import logging
import moment
import datetime
from statistics import mean
from exporter import config
from exporter import bucket
from exporter.utils import decorators
from exporter.utils import context_managers
from exporter.utils import func

logger = logging.getLogger(__name__)


class ExportWriter:
    def __init__(self):
        self.files_saved = []

    def update_old_rows(self, writer, old_file, data):
        for row in csv.DictReader(old_file):
            try:
                key = self.get_key(row, data)
                export_data = data.pop(key)
                writer.writerow(self.get_row(key, export_data))
            except (StopIteration, KeyError):
                writer.writerow(row)

    def get_key(self, row, data):
        try:
            _, second_key = next(iter(data))
            return row["date"], second_key
        except ValueError:
            return row["date"]

    def get_date(self, key):
        try:
            date, _ = key
            return date
        except ValueError:
            return key

    def write_new_rows(self, writer, export_data):
        for key, data in export_data.items():
            writer.writerow(self.get_row(key, data))

    def get_row(self, key, data):
        date = self.get_date(key)
        return {"date": date, **{key: value for key, value in data.items()}}

    def export_data(self, data, filename, field_list):
        data_copy = copy.copy(data)
        func.touch(filename)
        with context_managers.update_file(filename) as (old_file, temp_file):
            writer = csv.DictWriter(
                temp_file, fieldnames=field_list, extrasaction="ignore"
            )
            writer.writeheader()
            try:
                self.update_old_rows(writer, old_file, data_copy)
                self.write_new_rows(writer, data_copy)
            except StopIteration:
                pass
        self.sort_export_by_date(filename, field_list)
        self.files_saved.append(filename)

    def sort_export_by_date(self, filename, field_list):
        with context_managers.update_file(filename) as (old_file, temp_file):
            reader = csv.DictReader(old_file)
            sorted_rows = sorted(reader, key=lambda k: k["date"])
            writer = csv.DictWriter(temp_file, fieldnames=field_list)
            writer.writeheader()
            for row in sorted_rows:
                writer.writerow(row)

    def get_exported_data(self, filename):
        exported_data = {}
        with open(filename, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                date = row.pop("date")
                exported_data[date] = row
        return exported_data

    def get_first_day_of_the_week(self, formated_date):
        date = moment.date(formated_date).date
        first_day = date - datetime.timedelta(days=date.weekday())
        return first_day.strftime(config.DATE_FORMAT)

    def get_first_day_of_the_month(self, formated_date):
        return (
            moment.date(formated_date).date.replace(day=1).strftime(config.DATE_FORMAT)
        )

    def export_aggregated(
        self, filename, date_func, data, aggregate_func, number_type, field_list
    ):
        aggregated_data = {}
        for formated_date, row in data.items():
            date = date_func(formated_date)
            aggregated_row = aggregated_data.setdefault(date, {})
            self.aggregate_data_in_list(row, aggregated_row, number_type)
        self.aggregate_data(aggregated_data, aggregate_func)
        self.export_data(aggregated_data, filename, field_list)

    def aggregate_data_in_list(self, row, aggregated_row, number_type):
        for key, value in row.items():
            if value and float(value) != 0:
                aggregated_row.setdefault(key, []).append(
                    number_type(value) if "average" not in key else float(value)
                )

    def aggregate_data(self, data, aggregate_func):
        for date, values in data.items():
            for key, value_list in values.items():
                value = (
                    aggregate_func(value_list)
                    if "average" not in key
                    else mean(value_list)
                )
                data[date][key] = round(value, 2)

    @decorators.retry(bucket.UploadFailed, tries=config.TASK_TRIES, logger=logger)
    def upload_files(self):
        bucket_name = config.AWS_S3_BUCKET_NAME
        aws_bucket = bucket.BucketAws(bucket_name)
        for filename in self.files_saved:
            object_name = filename.split("/")[-1]
            aws_bucket.upload_file(filename, object_name)
