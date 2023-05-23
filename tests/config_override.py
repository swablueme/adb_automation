import os
import pathlib
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../screenshot")


class CONFIGURATION:
    IMAGE_MATCHING_TEMPLATE_FOLDER = "C:\\Users\\Destiny Chan\\Documents\\Actual Scripts\\opencv_cached_bot\\tests\\images"
    IMAGE_DEBUG_FOLDER = os.path.join(IMAGE_MATCHING_TEMPLATE_FOLDER, "debug")


pathlib.Path(CONFIGURATION.IMAGE_MATCHING_TEMPLATE_FOLDER).mkdir(
    parents=True, exist_ok=True)

pathlib.Path(CONFIGURATION.IMAGE_DEBUG_FOLDER).mkdir(
    parents=True, exist_ok=True)
