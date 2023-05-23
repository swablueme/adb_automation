from unittest import mock
from tests.utility import assertNotRaises
from parameterized import parameterized
import config_override
import unittest
from image_similarity import *
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../screenshot")


class TestImageFile(unittest.TestCase):
    @parameterized.expand([("button.png"),
                           ("base.png")])
    @mock.patch("image_similarity.config", config_override)
    def test_when_image_path_provided_should_produce_valid_image(self, image):
        button_image = assertNotRaises(
            ImageFile, image)
        self.assertEqual(int, type(button_image.get_height()))
        self.assertEqual(int, type(button_image.get_width()))
        self.assertTrue(True, ImageConversion.NumpytoPIL(
            button_image.get_image()).verify())


if __name__ == '__main__':
    unittest.main(verbosity=2)
