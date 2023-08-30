import os
import pathlib
import sys
from unittest import mock

sys.path.append(os.path.dirname(
    os.path.realpath(__file__)) + "\\..\\screenshot")


class CONFIGURATION:
    IMAGE_MATCHING_TEMPLATE_FOLDER = "C:\\Users\\Destiny Chan\\Documents\\Actual Scripts\\opencv_cached_bot\\tests\\images"
    IMAGE_DEBUG_FOLDER = os.path.join(IMAGE_MATCHING_TEMPLATE_FOLDER, "debug")
    MEMU_EMULATOR_NAME = "emulator-5554"


class TIMEOUTS:
    TIMEOUT_UNTIL_IMAGE_FIND_OPERATION_CANCELLED = 3
    SLEEP_INTERVAL_AFTER_TAP = 0.6


patcher = mock.patch("image.config.CONFIGURATION", CONFIGURATION)
patcher.start()

patcher2 = mock.patch("adb.config.TIMEOUTS", TIMEOUTS)
patcher2.start()

import image
import adb

pathlib.Path(CONFIGURATION.IMAGE_MATCHING_TEMPLATE_FOLDER).mkdir(
    parents=True, exist_ok=True)

pathlib.Path(CONFIGURATION.IMAGE_DEBUG_FOLDER).mkdir(
    parents=True, exist_ok=True)
