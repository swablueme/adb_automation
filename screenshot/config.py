import os
import pathlib


class CONFIGURATION:
    IMAGE_MATCHING_TEMPLATE_FOLDER = "C:\\Users\\Destiny Chan\\Documents\\Actual Scripts\\opencv cached bot\\screenshot\\images"
    IMAGE_DEBUG_FOLDER = os.path.join(IMAGE_MATCHING_TEMPLATE_FOLDER, "debug")


pathlib.Path(CONFIGURATION.IMAGE_MATCHING_TEMPLATE_FOLDER).mkdir(
    parents=True, exist_ok=True)

pathlib.Path(CONFIGURATION.IMAGE_DEBUG_FOLDER).mkdir(
    parents=True, exist_ok=True)
