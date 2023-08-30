import os
import pathlib


class CONFIGURATION:
    IMAGE_MATCHING_TEMPLATE_FOLDER = "C:\\Users\\Destiny Chan\\Documents\\Actual Scripts\\opencv_cached_bot\\screenshot\\images"
    IMAGE_DEBUG_FOLDER = os.path.join(IMAGE_MATCHING_TEMPLATE_FOLDER, "debug")
    MEMU_EMULATOR_NAME = "emulator-5554"


class TIMEOUTS:
    TIMEOUT_UNTIL_IMAGE_FIND_OPERATION_CANCELLED = 5
    SLEEP_INTERVAL_AFTER_TAP = 0.6


pathlib.Path(CONFIGURATION.IMAGE_MATCHING_TEMPLATE_FOLDER).mkdir(
    parents=True, exist_ok=True)

pathlib.Path(CONFIGURATION.IMAGE_DEBUG_FOLDER).mkdir(
    parents=True, exist_ok=True)
