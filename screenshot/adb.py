from __future__ import annotations
from adbutils import adb
import numpy as np
import time

from image import ImageFile
from image_similarity import *


class PhoneADB:
    # TODO: make sure adb is started first :(
    # https://stackoverflow.com/questions/14134892/convert-image-from-pil-to-opencv-format
    SLEEP_INTERVAL = 1

    def __init__(self):
        self.device = adb.device("emulator-5554")
        time.sleep(PhoneADB.SLEEP_INTERVAL)

    def screenshot(self) -> ImageFile:
        return ImageFile(self.device.screenshot())

    def click(self, x: int, y: int) -> None:
        self.device.click(x, y)

    def swipe(self, sx: int, sy: int, ex: int, ey: int, duration: float = 1.0) -> None:
        self.device(sx, sy, ex, ey, duration)


if __name__ == "__main__":
    pass
    # d.click(418, 191)
