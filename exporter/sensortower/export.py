import requests
import logging
import time
from requests import exceptions
from exporter import config
from exporter.utils import decorators

logger = logging.getLogger(__name__)


class SensorTowerApiCallsLimit(Exception):
    pass


class SensorTowerExport:
    request_limit = config.SENSORTOWER_REQUEST_LIMIT

    def __init__(self):
        self.request_counter = 0

    @decorators.retry(exceptions.ConnectionError,
                      tries=config.REQUEST_RETRIES,
                      delay=config.REQUEST_RETRY_DELAY,
                      logger=logger)
    def request_data(self, endpoint, params):
        self.update_request_counter()
        response = self.get(endpoint, params)
        response.raise_for_status()
        return response.json()

    def get(self, endpoint, params):
        time.sleep(config.SENSORTOWER_REQUEST_DELAY)
        return requests.get(
            f'{config.SENSORTOWER_ENDPOINT_BASE}{endpoint}',
            params=params,  
            timeout=5,
        )

    def update_request_counter(self):
        self.request_counter += 1
        if self.request_counter >= self.request_limit:
            raise SensorTowerApiCallsLimit
