
import time
import config


def timer(func):
    def wrapper_function(*args, **kwargs):
        t0 = time.time()
        results = func(*args, **kwargs)
        t1 = time.time()
        print(f"time taken for image similarity {func.__name__} {t1-t0}")
        return results
    return wrapper_function
