from unittest.result import failfast


def assertNotRaises(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        failfast(e.with_traceback())
