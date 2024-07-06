import os
import yaml
from pathlib import Path


def config_generator(path='../resources/config.yaml'):
    filepath = Path(__file__).parent / path
    with open(filepath, 'r') as file:
        return yaml.safe_load(file)


def get_script_location():
    return os.path.realpath(os.path.dirname(__file__))
