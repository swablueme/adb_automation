from __future__ import annotations
import random
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
            (top_left_x, top_left_y,
             width, height) = match_rectangle

            newWidth = self.scaling_factor * width
            newHeight = self.scaling_factor * height
            newX = top_left_x + width / 2 - newWidth / 2
            newY = top_left_y + height / 2 - newHeight / 2
            self.scaled_matches.append(
                (round(newX), round(newY), round(newWidth), round(newHeight)))
        return self

    def _get_centres_of_scaled_rectangles(self):
        for match_rectangle in self.match_rectangles:
            (top_left_x, top_left_y,
             width, height) = match_rectangle
            centre_x = top_left_x + width / 2
            centre_y = top_left_y + height / 2
            self.centres.append((round(centre_x), round(centre_y)))
        return self

    def get_scaled_match_rectangles(self):
        return self.scaled_matches

    def get_original_match_rectangles(self):
        return self.match_rectangles

    def get_centres(self):
        return self.centres

    def get_random_coords(self):
        random_coords = []
        for scaled_match in self.scaled_matches:
            (top_left_x, top_left_y,
             width, height) = scaled_match
            rand_x = random.randint(top_left_x, top_left_x + width)
            rand_y = random.randint(top_left_y, top_left_y + height)
            random_coords.append((rand_x, rand_y))

        return random_coords
