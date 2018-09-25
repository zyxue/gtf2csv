import logging
import time
from functools import update_wrapper


logger = logging.getLogger(__name__)


def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d


@decorator
def timeit(f):
    """time a function, used as decorator"""
    def new_f(*args, **kwargs):
        bt = time.time()
        r = f(*args, **kwargs)
        et = time.time()
        logger.info("time spent on {0}: {1:.2f}s".format(f.__name__, et - bt))
        return r
    return new_f
