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

        if self.image.shape is None:
            raise Exception(
                f"Image was a None value!")

        self.height = self.image.shape[:-1][0]
        self.width = self.image.shape[:-1][1]

    def get_image(self) -> np.ndarray:
        return self.image

    def get_width(self) -> int:
        return self.width

    def get_height(self) -> int:
        return self.height

    def view(self) -> None:
        Visualise.view_image(self)


class MatchType(Enum):
    COLOUR = 1
    GRAYSCALE = 0


class ImageSimilarity:
    def __init__(self, needle: ImageFile, image_to_search: ImageFile):
        self.match_coords = []
        self.needle = needle
        self.searched_image = image_to_search
        self.match_rectangles = []

    @timer
    def find_all_matches(self, match_type: MatchType = MatchType.GRAYSCALE, threshold: int = 0.95) -> ImageSimilarity:
        if match_type == MatchType.GRAYSCALE:
            results = self.monochrome_match()
            self.match_coords = np.where(results >= threshold)
            self.match_coords = list(zip(*self.match_coords[::-1]))
            self.generate_match_rectangles()
        elif match_type == MatchType.COLOUR:
            results = self.colour_match()
            total_results = {}
            for result_channel_name, results_for_channel in results.items():
                match_coords = np.where(results_for_channel >= threshold)
                match_coords = list(zip(*match_coords[::-1]))
                total_results[result_channel_name] = match_coords
            intersected_results = set(
                total_results["R"]).intersection(total_results["B"])
            intersected_results = intersected_results.intersection(
                total_results["G"])
            self.match_coords = list(intersected_results)
            self.generate_match_rectangles()
        return self

    @timer
    def find_best_match(self, match_type: MatchType = MatchType.GRAYSCALE) -> ImageSimilarity:
        if match_type == MatchType.GRAYSCALE:
            results = self.monochrome_match()
        elif match_type == MatchType.COLOUR:
            results = self.colour_match()
            results = results["R"] + results["B"] + results["G"]
        _, _, _, best_match = cv2.minMaxLoc(results)
        self.match_coords = np.array([best_match])
        self.generate_match_rectangles()

        return self

    def colour_match(self) -> Mat:
        # Split both into each R, G, B Channel
        imageMainR, imageMainG, imageMainB = cv2.split(
            self.searched_image.get_image())
        imageNeedleR, imageNeedleG, imageNeedleB = cv2.split(
            self.needle.get_image())

        # Matching each channel
        resultR = cv2.matchTemplate(
            imageMainR, imageNeedleR, cv2.TM_CCOEFF_NORMED)
        resultG = cv2.matchTemplate(
            imageMainG, imageNeedleG, cv2.TM_CCOEFF_NORMED)
        resultB = cv2.matchTemplate(
            imageMainB, imageNeedleB, cv2.TM_CCOEFF_NORMED)

        return {"B": resultB, "G": resultG, "R": resultR}

    def monochrome_match(self) -> Mat:
        return cv2.matchTemplate(
            self.searched_image.get_image(), self.needle.get_image(), cv2.TM_CCOEFF_NORMED)

    def generate_match_rectangles(self) -> None:
        for (match_x, match_y) in self.match_coords:
            match = (match_x, match_y,
                     self.needle.get_width(), self.needle.get_height())
            # https://learncodebygaming.com/blog/grouping-rectangles-into-click-points
            # lone match results will be disregarded, add it twice to prevent this
            self.match_rectangles.append(match)
            self.match_rectangles.append(match)

        self.match_rectangles, _ = cv2.groupRectangles(
            self.match_rectangles, groupThreshold=1, eps=0.05)
        return self

    def save_image(self, file_name="debug") -> ImageSimilarity:
        # debug method to write an image to a file location
        image = Visualise.draw_match_rectangles(self.searched_image,
                                                self.match_rectangles)
        Visualise.save_image(image, file_name)
        return self

    def view_image(self) -> ImageSimilarity:
        # debug method to write an image to a file location
        image = Visualise.draw_match_rectangles(self.searched_image,
                                                self.match_rectangles)
        Visualise.view_image(image)
        return self

    def get_matches(self):
        return self.match_rectangles


class Visualise:
    RED = (0, 0, 255)
    GREEN = (0, 255, 0)
    BLUE = (255, 0, 0)

    LINE_THICKNESS = 1
    POINT_RADIUS = 1

    @staticmethod
    def draw_match_rectangles(image: ImageFile, match_rectangles: list[tuple(int)], color: tuple[int] = RED) -> ImageFile:
        for rectangle in match_rectangles:
            (x, y, w, h) = rectangle
            cv2.rectangle(image.get_image(),
                          (x, y),
                          (x + w, y + h),
                          color=color,
                          thickness=Visualise.LINE_THICKNESS)
        return image

    @staticmethod
    def draw_circle(image: ImageFile, coords: list[tuple[int]], radius: int, color: tuple[int] = RED) -> ImageFile:
        for coord in coords:
            cv2.circle(image.get_image(), coord, radius,
                       color=color, thickness=Visualise.LINE_THICKNESS)
        return image

    @staticmethod
    def draw_point(image: ImageFile, coords: list[tuple[int]], color: tuple[int] = RED) -> ImageFile:
        for coord in coords:
            cv2.circle(image.get_image(), coord, Visualise.POINT_RADIUS,
                       color=color, thickness=Visualise.LINE_THICKNESS)
        return image

    @staticmethod
    def save_image(image: ImageFile, file_name: str = "debug") -> ImageFile:
        cv2.imwrite(os.path.join(config.CONFIGURATION.IMAGE_DEBUG_FOLDER,
                    file_name + ".png"), image.get_image())
        return image

    @staticmethod
    def view_image(image: ImageFile) -> None:
        ImageConversion.NumpytoPIL(image.get_image()).show()


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
