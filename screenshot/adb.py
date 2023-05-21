from adbutils import adb
import numpy as np
from PIL import Image
import time
import os
import cv2


class ImageMatching:
    IMAGE_PATH = "images"

    def test():
        base_path = os.path.join(os.getcwd(), "screenshot", "images")
        print(base_path)
        img_rgb = cv2.imread(os.path.join(
            base_path, 'base.png'))
        template = cv2.imread(os.path.join(
            base_path,  'button.png'))

        h, w = template.shape[:-1]
        res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)

        threshold = .95
        loc = np.where(res >= threshold)

        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

        cv2.imwrite(os.path.join(base_path, 'result.png'), img_rgb)


class ImageConversion:

    @staticmethod
    def PILtoNumpy(img: Image) -> np.ndarray:
        img.show()
        pilimg = img.convert('RGB')
        open_cv_image = np.asarray(pilimg)
        return open_cv_image


class PhoneADB:
    # TODO: make sure adb is started first :(
    # https://stackoverflow.com/questions/14134892/convert-image-from-pil-to-opencv-format
    SLEEP_INTERVAL = 3

    def __init__(self):
        self.device = adb.device()
        time.sleep(PhoneADB.SLEEP_INTERVAL)

    def screenshot(self) -> np.ndarray:
        return ImageConversion.PILtoNumpy(self.device.screenshot())

    def click(self, x, y):
        self.device.click(x, y)

    def swipe(self, sx, sy, ex, ey, duration: float = 1.0):
        self.device(sx, sy, ex, ey, duration)


if __name__ == "__main__":
    # PhoneADB().screenshot()
    ImageMatching.test()
    # d.click(418, 191)
