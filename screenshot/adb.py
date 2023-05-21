from __future__ import annotations
from typing import Union
from adbutils import adb
import numpy as np
from PIL.Image import Image
import time
import os
import cv2
import config


class ImageFile:
    def __init__(self, image_value: Union[str, Image]):

        self.image = None
        if type(image_value) == str:
            self.image = cv2.imread(os.path.join(
                config.CONFIGURATION.IMAGE_MATCHING_TEMPLATE_FOLDER, image_value))
        elif type(image_value) == Image:
            self.image = ImageConversion.PILtoNumpy(image_value)
        else:
            raise Exception(
                f"{image_value} must be an PIL image or a filepath(str) to a image!")

        self.height = self.image.shape[:-1][0]
        self.width = self.image.shape[:-1][1]

    def get_image(self):
        return self.image

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height


class ImageSimilarity:
    def __init__(self, match_template: ImageFile, image_to_search: ImageFile):
        self.match_locations = []
        self.match_template = match_template
        self.image_to_search = image_to_search

    def find_all_matches(self, threshold: int = 0.95) -> ImageSimilarity:
        results = cv2.matchTemplate(
            self.image_to_search.get_image(), self.match_template.get_image(), cv2.TM_CCOEFF_NORMED)
        self.match_locations = np.where(results >= threshold)
        self.match_locations = list(zip(*self.match_locations[::-1]))
        return self

    def find_best_match(self) -> ImageSimilarity:
        results = cv2.matchTemplate(
            self.image_to_search.get_image(), self.match_template.get_image(), cv2.TM_CCOEFF_NORMED)
        _, _, _, best_match = cv2.minMaxLoc(results)
        self.match_locations = [best_match]
        return self

    def visualise_results(self, file_name="debug.png") -> ImageSimilarity:
        # debug method to write an image to a file location
        RED = (0, 0, 255)
        for match_x, match_y in self.match_locations:
            cv2.rectangle(self.image_to_search.get_image(), (match_x, match_y),
                          (match_x + self.match_template.get_width(), match_y + self.match_template.get_height()), color=RED, thickness=2)

        cv2.imwrite(os.path.join(config.CONFIGURATION.IMAGE_DEBUG_FOLDER,
                    file_name), self.image_to_search.get_image())


class ImageConversion:

    @staticmethod
    def PILtoNumpy(img: Image) -> np.ndarray:
        img.show()
        pilimg = img.convert('RGB')
        open_cv_image = np.asarray(pilimg)
        return open_cv_image


class PhoneADB:
    # TODO: make sure adb is started first :(
    # https://stackoverflow.com/questions/14134892/convert-image-from-pil-to-opencv-format
    SLEEP_INTERVAL = 3

    def __init__(self):
        self.device = adb.device()
        time.sleep(PhoneADB.SLEEP_INTERVAL)

    def screenshot(self) -> np.ndarray:
        return ImageConversion.PILtoNumpy(self.device.screenshot())

    def click(self, x: int, y: int) -> None:
        self.device.click(x, y)

    def swipe(self, sx: int, sy: int, ex: int, ey: int, duration: float = 1.0) -> None:
        self.device(sx, sy, ex, ey, duration)


if __name__ == "__main__":
    # PhoneADB().screenshot()
    ImageSimilarity(ImageFile("button.png"), ImageFile(
        "base.png")).find_best_match().visualise_results()
    # d.click(418, 191)
