import sys
import os
from unittest import mock
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../screenshot")

import config_override

from utility import assertNotRaises
from image_similarity import *
import unittest


# @mock.patch("image_similarity.config", config_override)
class TestImageSimilarity(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestImageSimilarity, self).__init__(*args, **kwargs)
        patcher = mock.patch("image_similarity.config", config_override)
        patcher.start()
        self.button_image = ImageFile("button.png")
        self.base_image = ImageFile("base.png")

    def test_image_similarity_should_return_best_match(self):
        similarity = assertNotRaises(ImageSimilarity(
            self.button_image, self.base_image).find_best_match().visualise_matches, "best_image_results.png")
        self.assertEqual(1, len(similarity.match_coords))
        self.assertEqual(1, len(similarity.match_rectangles))

    def test_image_similarity_should_return_all_matches(self):
        similarity = assertNotRaises(ImageSimilarity(
            self.button_image, self.base_image).find_all_matches(match_type=MatchType.COLOUR).visualise_matches, "all_image_results.png")

        self.assertEqual(4, len(similarity.match_coords))
        self.assertEqual(3, len(similarity.match_rectangles))


if __name__ == '__main__':
    unittest.main(verbosity=2)
