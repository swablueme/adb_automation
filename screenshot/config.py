from pathlib import Path
from utilities import config_generator

config_settings = config_generator()

Path(config_settings["IMAGE_MATCHING_TEMPLATE_FOLDER"]).mkdir(
    parents=True, exist_ok=True)

Path(config_settings["IMAGE_DEBUG_FOLDER"]).mkdir(
    parents=True, exist_ok=True)
