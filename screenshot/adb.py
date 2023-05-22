from __future__ import annotations
from typing import Union
from adbutils import adb
import numpy as np
from PIL.Image import Image
import time
import os
import cv2
import config


class PhoneADB:
    # TODO: make sure adb is started first :(
    # https://stackoverflow.com/questions/14134892/convert-image-from-pil-to-opencv-format
    SLEEP_INTERVAL = 3

    def __init__(self):
        self.device = adb.device()
        time.sleep(PhoneADB.SLEEP_INTERVAL)

    def screenshot(self) -> np.ndarray:
        return ImageConversion.PILtoNumpy(self.device.screenshot())

    def click(self, x: int, y: int) -> None:
        self.device.click(x, y)

    def swipe(self, sx: int, sy: int, ex: int, ey: int, duration: float = 1.0) -> None:
        self.device(sx, sy, ex, ey, duration)


if __name__ == "__main__":
    # PhoneADB().screenshot()

    # d.click(418, 191)
