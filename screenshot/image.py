from PIL.Image import Image
import config
import cv2
import PIL
import os
from typing import Union
import numpy as np


class ImageFile:
    def __init__(self, image_value: Union[str, Image]):
        self.image = None
        if type(image_value) == str:
            self.image = cv2.imread(os.path.join(
                config.config_settings["IMAGE_MATCHING_TEMPLATE_FOLDER"], image_value))
        elif type(image_value) == Image:
            self.image = ImageConversion.PILtoNumpy(image_value)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR)
        else:
            raise Exception(
                f"{image_value} must be an PIL image or a filepath(str) to a image!")

        if self.image.shape is None:
            raise Exception(
                f"Image was a None value!")

        self.height = self.image.shape[:-1][0]
        self.width = self.image.shape[:-1][1]

    def get_image(self) -> np.ndarray:
        return self.image

    def get_width(self) -> int:
        return self.width

    def get_height(self) -> int:
        return self.height

    def view(self) -> None:
        Visualise.view_image(self)


class Visualise:
    RED = (0, 0, 255)
    GREEN = (0, 255, 0)
    BLUE = (255, 0, 0)

    LINE_THICKNESS = 1
    POINT_RADIUS = 1

    @staticmethod
    def draw_match_rectangles(image: ImageFile, match_rectangles: list[tuple[int]], color: tuple[int] = RED) -> ImageFile:
        for rectangle in match_rectangles:
            (x, y, w, h) = rectangle
            cv2.rectangle(image.get_image(),
                          (x, y),
                          (x + w, y + h),
                          color=color,
                          thickness=Visualise.LINE_THICKNESS)
        return image

    @staticmethod
    def draw_circle(image: ImageFile, coords: list[tuple[int]], radius: int, color: tuple[int] = RED) -> ImageFile:
        for coord in coords:
            cv2.circle(image.get_image(), coord, radius,
                       color=color, thickness=Visualise.LINE_THICKNESS)
        return image

    @staticmethod
    def draw_point(image: ImageFile, coords: list[tuple[int]], color: tuple[int] = RED) -> ImageFile:
        for coord in coords:
            cv2.circle(image.get_image(), coord, Visualise.POINT_RADIUS,
                       color=color, thickness=Visualise.LINE_THICKNESS)
        return image

    @staticmethod
    def save_image(image: ImageFile, file_name: str = "debug") -> ImageFile:
        cv2.imwrite(os.path.join(config.config_settings["IMAGE_DEBUG_FOLDER"],
                    file_name + ".png"), image.get_image())
        return image

    @staticmethod
    def view_image(image: ImageFile) -> None:
        ImageConversion.NumpytoPIL(image.get_image()).show()


class ImageConversion:
    @staticmethod
    def PILtoNumpy(img: Image) -> np.ndarray:
        # img.show()
        pilimg = img.convert('RGB')
        # BGR conversion
        open_cv_image = np.asarray(pilimg)
        return open_cv_image

    @staticmethod
    def NumpytoPIL(img: np.ndarray) -> Image:
        imageRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return PIL.Image.fromarray(imageRGB)
