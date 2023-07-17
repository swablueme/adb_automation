import config_override
import unittest
from click_region import *
from image_similarity import *


class TestClickRegion(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestClickRegion, self).__init__(*args, **kwargs)

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
                test_data_click_region.get_scaled_match_rectangles(), color=Visualise.GREEN)
            Visualise.draw_point(
                test_data, test_data_click_region.get_centres())

            for _ in range(200):
                Visualise.draw_point(
                    test_data, test_data_click_region.get_random_coords(), color=Visualise.BLUE)

            Visualise.save_image(
                test_data, self.__class__.__name__ + self._testMethodName + "_" + str(idx))

    def test_should_find_rectangle_centre(self):
        self.assertEqual(
            [(109, 43)], self.blank_image_click_region.get_centres())
        self.assertEqual(
            [(354, 1204), (354, 1534)],
            self.base_image_click_region.get_centres())

    def test_rectangle_should_scale(self):
        self.assertEqual(
            [(44, 17, 131, 52)], self.blank_image_click_region.get_scaled_match_rectangles())
        self.assertEqual(
            [(303, 1183, 104, 41), (303, 1513, 104, 41)],
            self.base_image_click_region.get_scaled_match_rectangles())


if __name__ == '__main__':
    unittest.main(verbosity=3)
