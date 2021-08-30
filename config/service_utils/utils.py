import redis
import pickle
import os
import time
import pandas as pd
import numpy as np

from django.conf import settings

redis_obj = redis.StrictRedis(settings.REDIS_HOST)
csv_path = os.path.dirname(os.path.abspath(__package__)) + '/data_files/csv/'


class NoExceptions(Exception):
    """Dummy exception, never raised"""


def get_csv(name):
    """
    It returns the cached CSV data
    :param name:
    :return:
    """
    key_name = 'analytics_{}'.format(name)
    if not redis_obj.exists(key_name) or redis_obj.get(key_name) is None:
        csv_name = "{}.csv".format(name)
        csv_df = pd.read_csv(csv_path + csv_name)
        csv_df.columns = csv_df.columns.str.strip()
        pickled_object = pickle.dumps(csv_df)
        redis_obj.set(key_name, pickled_object)
        unpacked_csv_obj = csv_df
    else:
        unpacked_csv_obj = pickle.loads(redis_obj.get(key_name))
    return unpacked_csv_obj


def set_with_na_check(value, default_value, reduce_func=None,
                      accept_exceptions=(NoExceptions, ), exception_value=None):
    """
    Returns default_value if value is 'NA' else returns value itself
    Also reduces value to scalar if reduce func is defined and add options to catch errors
    """
    try:
        if exception_value is None:
            exception_value = default_value
        if reduce_func is not None and callable(reduce_func):
            value = reduce_func(value)
        if pd.isna(value):
            return default_value
    except accept_exceptions:
        return exception_value

    return value


def clean_name_lower(name):
    """
    Filter to only alpha numeric characters and return its lower
    :param name: string to clean
    :return: clean string
    """
    return ''.join(e for e in name.lower() if e.isalnum())


def safe_divide(dividend, divisor, default=np.NaN, fillna=np.NaN):
    """
    Safely divide a number with zero division check
    """
    try:
        result = float(dividend)/float(divisor)
        if pd.isna(result) or result == np.inf or result == -np.inf:
            return fillna
        return result
    except ZeroDivisionError:
        return default


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result
    return timed
