from exporter import config
from exporter.utils import executor


class Executor(executor.Executor):
    source_name = 'sensortower'
    apps = config.SENSORTOWER_APPS
