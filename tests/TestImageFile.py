from tests.utility import assertNotRaises
from parameterized import parameterized
import config_override
import unittest
from image import ImageConversion
from image_similarity import *


class TestImageFile(unittest.TestCase):

    @parameterized.expand([("button.png"),
                           ("base.png")])
    def test_when_image_path_provided_should_produce_valid_image(self, image):
        button_image = assertNotRaises(
            ImageFile, image)
        self.assertEqual(int, type(button_image.get_height()))
        self.assertEqual(int, type(button_image.get_width()))
        self.assertTrue(True, ImageConversion.NumpytoPIL(
            button_image.get_image()).verify())


if __name__ == '__main__':
    unittest.main(verbosity=2)
