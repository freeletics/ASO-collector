import os


def touch(filename):
    with open(filename, "a"):
        os.utime(filename, None)