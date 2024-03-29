from __future__ import annotations
from enum import Enum
from cv2 import Mat
import numpy as np
import cv2
import time
from annotations import timer
from image import ImageFile, Visualise


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

            # valid matches should be found if the similarity is there for all three of the red, blue and green channels
            # because otherwise one area might perform really good on red and another might perform really good on blue
            # and the poor performance on one colour might be cancelled out by another
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
