from __future__ import annotations
import numpy as np


class ClickRegion:
    def __init__(self, match_rectangles, scaling_factor: float = 0.6):
        self.match_rectangles = match_rectangles
        self.scaled_matches = []
        self.scaling_factor = scaling_factor
        self.centres = []
        self._scale_region()
        self._get_centres_of_scaled_rectangles()

    def _scale_region(self) -> ClickRegion:
        for match_rectangle in self.match_rectangles:
            (bottom_left_x, bottom_left_y,
             width, height) = match_rectangle

            newWidth = self.scaling_factor * width
            newHeight = self.scaling_factor * height
            newX = bottom_left_x + width / 2 - newWidth / 2
            newY = bottom_left_y / 2 - newHeight / 2
            self.scaled_matches.append(
                (round(newX), round(newY), round(newWidth), round(newHeight)))
        return self

    def _get_centres_of_scaled_rectangles(self):
        for match_rectangle in self.match_rectangles:
            (bottom_left_x, bottom_left_y,
             width, height) = match_rectangle
            centre_x = bottom_left_x + width / 2
            centre_y = height / 2
            self.centres.append((round(centre_x), round(centre_y)))

    def get_scaled_match_rectangles(self):
        return self.scaled_matches

    def get_original_match_rectangles(self):
        return self.match_rectangles

    def get_centres(self):
        return self.centres

    # def randomise_click_coordinates(self):
