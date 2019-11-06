import os
import csv
import moment


def touch(filename):
    with open(filename, "a"):
        os.utime(filename, None)


def get_last_date(export_from, filename):
    try:
        with open(filename, mode="r") as file:
            reader = csv.DictReader(file)
            return max([moment.date(row["date"]).date for row in reader])
    except (ValueError, FileNotFoundError):
        return export_from


def convertion_rate(downloads, denominator):
    try:
        return round(int(downloads) / int(denominator) * 100, 2)
    except ZeroDivisionError:
        return None
