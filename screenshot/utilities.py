import os


def get_script_location():
    return os.path.realpath(os.path.dirname(__file__))
