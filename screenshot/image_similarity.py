from __future__ import annotations
from typing import Union
import PIL
from cv2 import Mat
import numpy as np
from PIL.Image import Image
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
    def __init__(self, needle: ImageFile, image_to_search: ImageFile):
        self.match_locations = []
        self.needle = needle
        self.image_to_search = image_to_search

    def find_all_matches(self, threshold: int = 0.95) -> ImageSimilarity:

        results = self.monochrome_match()
        self.match_locations = np.where(results >= threshold)

        self.match_locations = list(zip(*self.match_locations[::-1]))
        return self

    def find_best_match(self) -> ImageSimilarity:

        results = self.monochrome_match()
        _, _, _, best_match = cv2.minMaxLoc(results)
        self.match_locations = [best_match]
        return self

    def monochrome_match(self) -> Mat:
        return cv2.matchTemplate(
            self.image_to_search.get_image(), self.needle.get_image(), cv2.TM_CCOEFF_NORMED)

    def visualise_results(self, file_name="debug.png") -> ImageSimilarity:
        # debug method to write an image to a file location
        RED = (0, 0, 255)
        for match_x, match_y in self.match_locations:
            cv2.rectangle(self.image_to_search.get_image(), (match_x, match_y),
                          (match_x + self.needle.get_width(), match_y + self.needle.get_height()), color=RED, thickness=2)

        cv2.imwrite(os.path.join(config.CONFIGURATION.IMAGE_DEBUG_FOLDER,
                    file_name), self.image_to_search.get_image())
        return self


class ImageConversion:
    @staticmethod
    def PILtoNumpy(img: Image) -> np.ndarray:
        # img.show()
        pilimg = img.convert('RGB')
        open_cv_image = np.asarray(pilimg)
        return open_cv_image

    @staticmethod
    def NumpytoPIL(img:  np.ndarray) -> Image:
        return PIL.Image.fromarray(img)
