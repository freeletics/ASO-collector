from contextlib import contextmanager
import shutil
import tempfile as tempfile_module


@contextmanager
def update_file(filename):
    tempfile = tempfile_module.NamedTemporaryFile(mode="w", delete=False)
    with open(filename, mode="r") as file, tempfile:
        yield file, tempfile
    shutil.move(tempfile.name, filename)
