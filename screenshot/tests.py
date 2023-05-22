import unittest
from unittest import suite
from unittest.result import failfast
from image_similarity import *
from parameterized import parameterized


def assertNotRaises(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        failfast(e.with_traceback())


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


class TestImageMethods(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestImageMethods, self).__init__(*args, **kwargs)
        self.button_image = ImageFile("button.png")
        self.base_image = ImageFile("base.png")

    def test_image_similarity_should_return_best_match(self):
        similarity = assertNotRaises(ImageSimilarity(
            self.button_image, self.base_image).find_best_match)

        self.assertEqual(1, len(similarity.match_locations))

    def test_image_similarity_should_return_all_matches(self):
        similarity = assertNotRaises(ImageSimilarity(
            self.button_image, self.base_image).find_all_matches().visualise_results)
        print(similarity.match_locations)
        self.assertEqual(3, len(similarity.match_locations))


if __name__ == '__main__':
    unittest.main(verbosity=2)
