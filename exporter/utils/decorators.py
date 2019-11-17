import time
from functools import wraps
from exporter import config


def retry(exceptions, tries=4, delay=3, backoff=2, logger=None):
    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except exceptions as e:
                    msg = "{}, Retrying in {} seconds...".format(e, mdelay)
                    if logger:
                        logger.warning(msg)
                    else:
                        print(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry

    return deco_retry


def catch_task_error(name, logger):
    def catch(func):
        def wrapper(*args, **kwargs):
            logger.info("{} task".format(name))
            try:
                func(*args, **kwargs)
            except Exception as e:
                if logger:
                    logger.error("{} task failed".format(name))
                    logger.error(e)
                print(e)
                if config.DEBUG:
                    raise e
        return wrapper
    return catch
