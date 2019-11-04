import os


def touch(filename):
    with open(filename, "a"):
        os.utime(filename, None)


def convertion_rate(downloads, denominator):
    try:
        return round(int(downloads) / int(denominator) * 100, 2)
    except ZeroDivisionError:
        return None
