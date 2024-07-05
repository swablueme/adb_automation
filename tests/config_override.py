

import pathlib
from unittest import mock
import sys
import os
sys.path.append(os.path.dirname(
    os.path.realpath(__file__)) + "\\..\\screenshot")


class CONFIGURATION:
    IMAGE_MATCHING_TEMPLATE_FOLDER = "C:\\Users\\Destiny Chan\\Documents\\Actual Scripts\\opencv_cached_bot\\tests\\images"
    IMAGE_DEBUG_FOLDER = os.path.join(IMAGE_MATCHING_TEMPLATE_FOLDER, "debug")
    MEMU_EMULATOR_NAME = "emulator-5554"
    PHONE_NAME = "19241FDF6007JL"


class TIMEOUTS:
    TIMEOUT_UNTIL_IMAGE_FIND_OPERATION_CANCELLED = 3
    SLEEP_INTERVAL_AFTER_TAP = 0.6


patcher = mock.patch("image.config.CONFIGURATION", CONFIGURATION)
patcher.start()

patcher2 = mock.patch("adb.config.TIMEOUTS", TIMEOUTS)
patcher2.start()
import image  # nopep8
import adb  # nopep8
pathlib.Path(CONFIGURATION.IMAGE_MATCHING_TEMPLATE_FOLDER).mkdir(
    parents=True, exist_ok=True)

pathlib.Path(CONFIGURATION.IMAGE_DEBUG_FOLDER).mkdir(
    parents=True, exist_ok=True)

print(os.path.dirname(
    os.path.realpath(__file__)))
