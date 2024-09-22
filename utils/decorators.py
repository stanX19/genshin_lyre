import functools
import time

def retry_on_exception(exception_to_catch, max_retries=None):
    """
    A decorator that retries a function if a specified exception occurs.

    :param exception_to_catch: The exception type to catch (or a tuple of exceptions).
    :param max_retries: Maximum number of retries. If None, retries infinitely.
    """
    def decorator_retry(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while max_retries is None or attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except exception_to_catch:
                    attempts += 1
            raise e
        return wrapper
    return decorator_retry
