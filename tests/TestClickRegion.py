import config_override
import unittest
from unittest import mock
from click_region import *
from image_similarity import *

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
        self.blank_image_region = ClickRegion([(0, 86, 218, 86)])

    def test_should_find_rectangle_centre(self):
        self.assertEqual([(109, 43)], self.blank_image_region.get_centres())

    def test_rectangle_should_shrink(self):
        self.assertEqual(
            [(44, 17, 131, 52)], self.blank_image_region.get_scaled_match_rectangles())
        # image = Visualise.draw_match_rectangles(
        #     self.blank_image, click_regions)
        # image = Visualise.draw_point(
        #     image, centres)
        # Visualise.save_image(image, self._testMethodName)

    def test_should_shrink_all_matches_rectangle(self):
        rectangle_matches = assertNotRaises(ImageSimilarity(
            self.button_image, self.base_image).find_all_matches(match_type=MatchType.COLOUR)).get_matches()
        click_regions = [ClickRegion(rectangle)
                         for rectangle in rectangle_matches.get_matches()]
        self.assertEqual(3, len(click_regions))


if __name__ == '__main__':
    unittest.main(verbosity=3)
