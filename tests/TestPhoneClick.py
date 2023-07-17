
import config_override
from click_region import ClickRegion
from adb import *
import unittest


class TestPhoneClick(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestPhoneClick, self).__init__(*args, **kwargs)

    def testClick(self):
        device = PhoneADB()
        phone_screenshot = device.screenshot()
        phone_screenshot.view()
        # phone_screenshot = ImageFile("screenshot.png")
        self.app_icon = ImageFile("app_icon.png")

        matches = ImageSimilarity(
            self.app_icon, phone_screenshot).find_all_matches(match_type=MatchType.COLOUR).get_matches()

        test_data_click_region = ClickRegion(matches)

        Visualise.draw_match_rectangles(
            phone_screenshot,
            test_data_click_region.get_original_match_rectangles())
        Visualise.save_image(
            phone_screenshot, self.__class__.__name__ + self._testMethodName)


if __name__ == '__main__':
    unittest.main(verbosity=3)
