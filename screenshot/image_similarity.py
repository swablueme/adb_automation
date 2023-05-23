from __future__ import annotations
from enum import Enum
from typing import Union
import PIL
from cv2 import Mat
import numpy as np
from PIL.Image import Image
import os
import cv2
import config
import time


def timer(func):
    def wrapper_function(*args, **kwargs):
        t0 = time.time()
        results = func(*args, **kwargs)
        t1 = time.time()
        print(f"time taken for image similarity {func.__name__} {t1-t0}")
        return results
    return wrapper_function


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


class MatchType(Enum):
    COLOUR = 1
    GRAYSCALE = 0


class ImageSimilarity:
    def __init__(self, needle: ImageFile, image_to_search: ImageFile):
        self.match_coords = []
        self.needle = needle
        self.image_to_search = image_to_search
        self.match_rectangles = []

    @timer
    def find_all_matches(self, match_type: MatchType = MatchType.GRAYSCALE, threshold: int = 0.95) -> ImageSimilarity:
        if match_type == MatchType.GRAYSCALE:
            results = self.monochrome_match()
        elif match_type == MatchType.COLOUR:
            results = self.colour_match()
            threshold *= 3

        self.match_coords = np.where(results >= threshold)
        self.match_coords = np.array(list(zip(*self.match_coords[::-1])))
        self.generate_match_rectangles()

        return self

    @timer
    def find_best_match(self, match_type: MatchType = MatchType.GRAYSCALE) -> ImageSimilarity:
        if match_type == MatchType.GRAYSCALE:
            results = self.monochrome_match()
        elif match_type == MatchType.COLOUR:
            results = self.colour_match()

        results = self.monochrome_match()
        _, _, _, best_match = cv2.minMaxLoc(results)
        self.match_coords = np.array([best_match])
        self.generate_match_rectangles()
        return self

    def colour_match(self) -> Mat:
        # Split both into each R, G, B Channel
        imageMainR, imageMainG, imageMainB = cv2.split(
            self.image_to_search.get_image())
        imageNeedleR, imageNeedleG, imageNeedleB = cv2.split(
            self.needle.get_image())

        # Matching each channel
        resultR = cv2.matchTemplate(
            imageMainR, imageNeedleR, cv2.TM_CCOEFF_NORMED)
        resultG = cv2.matchTemplate(
            imageMainG, imageNeedleG, cv2.TM_CCOEFF_NORMED)
        resultB = cv2.matchTemplate(
            imageMainB, imageNeedleB, cv2.TM_CCOEFF_NORMED)

        # Add together to get the total score
        result = resultB + resultG + resultR
        return result

    def monochrome_match(self) -> Mat:
        return cv2.matchTemplate(
            self.image_to_search.get_image(), self.needle.get_image(), cv2.TM_CCOEFF_NORMED)

    def generate_match_rectangles(self) -> None:
        for (match_x, match_y) in self.match_coords:
            match = [match_x, match_y,
                     self.needle.get_width(), self.needle.get_height()]
            # https://learncodebygaming.com/blog/grouping-rectangles-into-click-points
            # lone match results will be disregarded, add it twice to prevent this
            self.match_rectangles.append(match)
            self.match_rectangles.append(match)

        self.match_rectangles, _ = cv2.groupRectangles(
            self.match_rectangles, groupThreshold=1, eps=0.05)
        return self

    def visualise_matches(self, file_name="debug.png") -> ImageSimilarity:
        # debug method to write an image to a file location
        RED = (0, 0, 255)
        for rectangle in self.match_rectangles:
            (x, y, w, h) = rectangle
            cv2.rectangle(self.image_to_search.get_image(),
                          (x, y),
                          (x + w, y + h),
                          color=RED,
                          thickness=1)

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
    def NumpytoPIL(img: np.ndarray) -> Image:
        imageRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return PIL.Image.fromarray(imageRGB)
