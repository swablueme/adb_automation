from unittest import mock
import config_override
from utility import assertNotRaises
from image_similarity import *
import unittest
from parameterized import parameterized


class TestImageSimilarity(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestImageSimilarity, self).__init__(*args, **kwargs)
        patcher = mock.patch("image_similarity.config", config_override)
        patcher.start()
        self.button_image = ImageFile("button.png")
        self.base_image = ImageFile("base.png")
        self.ark_path_image = ImageFile("pathtile.png")
        self.ark_base_image = ImageFile("basearknights.png")

    @parameterized.expand([MatchType.GRAYSCALE,
                           MatchType.COLOUR])
    def test_image_similarity_should_return_best_match(self, match_type):
        similarity = assertNotRaises(ImageSimilarity(
            self.button_image, self.base_image).find_best_match(match_type=match_type).save_image,
            self._testMethodName + str(match_type))
        self.assertEqual(1, len(similarity.match_coords))
        self.assertEqual(1, len(similarity.match_rectangles))

    def test_image_similarity_should_return_all_matches_grayscale(self):
        similarity = assertNotRaises(ImageSimilarity(
            self.button_image, self.base_image).find_all_matches(match_type=MatchType.GRAYSCALE).save_image,
            self._testMethodName)

        self.assertEqual(4, len(similarity.match_coords))
        self.assertEqual(3, len(similarity.match_rectangles))

    def test_image_similarity_should_return_all_matches_colour(self):
        similarity = assertNotRaises(ImageSimilarity(
            self.button_image, self.base_image).find_all_matches(match_type=MatchType.COLOUR).save_image,
            self._testMethodName)

        self.assertEqual(3, len(similarity.match_coords))
        self.assertEqual(2, len(similarity.match_rectangles))

    # @parameterized.expand([MatchType.GRAYSCALE,
    #                        MatchType.COLOUR])
    # def test_image_similarity_should_return_all_matches_arknights(self, match_type):
    #     similarity = assertNotRaises(ImageSimilarity(
    #         self.ark_path_image, self.ark_base_image).find_all_matches(match_type=match_type, threshold=0.8).save_image,
    #         self._testMethodName + str(match_type))

    #     self.assertEqual(4, len(similarity.match_coords))
    #     self.assertEqual(3, len(similarity.match_rectangles))


if __name__ == '__main__':
    unittest.main(verbosity=2)
