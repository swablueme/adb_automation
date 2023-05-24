import config_override
import unittest
from unittest import mock
from click_region import *
from image_similarity import *
import copy
from parameterized import parameterized
from tests.utility import assertNotRaises


class TestClickRegion(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestClickRegion, self).__init__(*args, **kwargs)
        patcher = mock.patch("image_similarity.config", config_override)
        patcher.start()

    def setUp(self) -> None:
        self.blank_image = ImageFile("blank.png")
        self.button_image = ImageFile("button.png")
        self.base_image = ImageFile("base.png")
        self.blank_image_click_region = ClickRegion([(0, 0, 218, 86)])

        self.base_matches = ImageSimilarity(
            self.button_image, self.base_image).find_all_matches(match_type=MatchType.COLOUR).get_matches()
        self.base_image_click_region = ClickRegion(self.base_matches)

    def test_visualise(self):
        for idx, (test_data, test_data_click_region) in enumerate([(self.blank_image, self.blank_image_click_region),
                                                                   (self.base_image, self.base_image_click_region)]):
            Visualise.draw_match_rectangles(
                test_data,
                test_data_click_region.get_original_match_rectangles())
            Visualise.draw_match_rectangles(
                test_data,
                test_data_click_region.get_scaled_match_rectangles())
            Visualise.draw_point(
                test_data, test_data_click_region.get_centres())
            Visualise.save_image(
                test_data, self.__class__.__name__ + self._testMethodName + "_" + str(idx))

    def test_should_find_rectangle_centre(self):
        self.assertEqual(
            [(109, 43)], self.blank_image_click_region.get_centres())
        self.assertEqual(
            [(354, 1204), (354, 1534), (354, 1864)], self.base_image_click_region.get_centres())

    def test_rectangle_should_shrink(self):
        self.assertEqual(
            [(44, 17, 131, 52)], self.blank_image_click_region.get_scaled_match_rectangles())

    def test_should_shrink_all_matches_rectangle(self):
        self.assertEqual(
            3, len(self.base_image_click_region.get_scaled_match_rectangles()))


if __name__ == '__main__':
    unittest.main(verbosity=3)
