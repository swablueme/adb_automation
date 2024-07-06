from unittest.result import failfast
import os
import shutil


def assertNotRaises(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        failfast(e.with_traceback())


def remove_folder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)
