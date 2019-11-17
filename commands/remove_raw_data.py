import os
import distutils.cmd
from exporter import config


class RemoveRawData(distutils.cmd.Command):
    description = 'clear raw data directory'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        raw_data_filenames = os.listdir(config.RAW_DATA_DIR)
        for filename in raw_data_filenames:
            os.remove(os.path.join(config.RAW_DATA_DIR, filename))
            print(f'Raw data file {filename} deleted')