import csv
import copy

from exporter import config
from exporter import bucket
from exporter.utils import context_managers
from exporter.utils import func


class ExportWriter:
    def __init__(self):
        self.files_saved = []

    def update_old_rows(self, writer, old_file, data):
        _, platform = next(iter(data))
        for row in csv.DictReader(old_file):
            try:
                key = self.get_key(row, platform)
                export_data = data.pop(key)
                writer.writerow(self.get_row(key, export_data))
            except KeyError:
                writer.writerow(row)

    def get_key(self, row, platform):
        return row["date"], platform

    def write_new_rows(self, writer, export_data):
        for key, data in export_data.items():
            writer.writerow(self.get_row(key, data))

    def get_row(self, key, data):
        date, platform = key
        return {
            "date": date,
            **{
                key: value
                for key, value in data.items()
            },
        }
    
    def export_data(self, data, filename, field_list):
        data_copy = copy.copy(data)
        func.touch(filename)
        with context_managers.update_file(filename) as (old_file, temp_file):
            writer = csv.DictWriter(temp_file, fieldnames=field_list)
            writer.writeheader()
            self.update_old_rows(writer, old_file, data_copy)
            self.write_new_rows(writer, data_copy)
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

    # TODO: retry logic on fail
    def upload_files(self):
        bucket_name = config.AWS_S3_BUCKET_NAME
        aws_bucket = bucket.BucketAws(bucket_name)
        for filename in self.files_saved:
            object_name = filename.split('/')[-1]
            aws_bucket.upload_file(filename, object_name)
            