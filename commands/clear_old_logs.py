import os
import distutils.cmd
import moment
from datetime import timedelta
from datetime import datetime
from exporter import config


class ClearOldLogs(distutils.cmd.Command):
    description = 'clear logs older then specified'
    user_options = [('days=', 'd', 'delete logs older then x days')]

    def initialize_options(self):
        self.days = 7

    def finalize_options(self):
        pass

    def run(self):
        LOGS_PATH = os.path.join(config.BASE_DIR, 'logs')
        log_files = os.listdir(LOGS_PATH)
        for filename in log_files:
            date = moment.date(filename.split('.')[0]).date
            if date and date + timedelta(days=self.days) < datetime.now():  
                os.remove(os.path.join(LOGS_PATH, filename))
                print(f'Log file {filename} deleted')