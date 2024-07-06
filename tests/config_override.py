
import pathlib
from unittest import mock
import sys
import os

sys.path.append(os.path.dirname(
    os.path.realpath(__file__)) + "\\..\\screenshot")

from utilities import config_generator  # nopep8
config_settings = config_generator("../resources/config-test.yaml")

patcher = mock.patch("image.config.config_settings", config_settings)
patcher.start()

patcher = mock.patch("adb.config.config_settings", config_settings)
patcher.start()


import image  # nopep8
import adb  # nopep8
pathlib.Path(config_settings["IMAGE_MATCHING_TEMPLATE_FOLDER"]).mkdir(
    parents=True, exist_ok=True)

pathlib.Path(config_settings["IMAGE_DEBUG_FOLDER"]).mkdir(
    parents=True, exist_ok=True)

print(os.path.dirname(
    os.path.realpath(__file__)))
