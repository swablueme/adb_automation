from __future__ import annotations
from adbutils import adb
import time

from image import ImageFile
from image_similarity import *
from click_region import ClickRegion
import config


class PhoneADB:
    # TODO: make sure adb is started first :(
    # https://stackoverflow.com/questions/14134892/convert-image-from-pil-to-opencv-format
    ADB_START_SLEEP_INTERVAL = 1
    SLEEP_INTERVAL_IMAGE_FIND = 0.2

    def __init__(self, device_name=config.CONFIGURATION.MEMU_EMULATOR_NAME):
        self.device = adb.device(
            device_name)

    def screenshot(self) -> ImageFile:
        return ImageFile(self.device.screenshot())

    def _found(self, needle: str, timeout, threshold, match_type) -> tuple(list, ImageFile):
        needle_img = ImageFile(needle)
        matches = []
        current_time = 0
        while current_time <= timeout:
            phone_screenshot = self.screenshot()
            matches = ImageSimilarity(
                needle_img, phone_screenshot).find_all_matches(match_type, threshold).get_matches()
            if len(matches) > 0:
                return matches, phone_screenshot
            time.sleep(PhoneADB.SLEEP_INTERVAL_IMAGE_FIND)
            current_time += PhoneADB.SLEEP_INTERVAL_IMAGE_FIND
        raise TimeoutError(
            f"PhoneADB._found function timed out as it reached {current_time} without finding a match which exceeds {config.TIMEOUTS.TIMEOUT_UNTIL_IMAGE_FIND_OPERATION_CANCELLED}")

    def wait_for_image(self, needle: str, timeout=config.TIMEOUTS.TIMEOUT_UNTIL_IMAGE_FIND_OPERATION_CANCELLED, threshold=0.85, match_type=MatchType.COLOUR):
        self._found(needle, timeout, threshold, match_type)

    def tap_image(self, needle: str, timeout=config.TIMEOUTS.TIMEOUT_UNTIL_IMAGE_FIND_OPERATION_CANCELLED, threshold=0.85, match_type=MatchType.COLOUR):
        try:
            matches, phone_screenshot = self._found(
                needle, timeout, threshold, match_type)

            matched_click_region = ClickRegion(matches)
            # Visualise.draw_match_rectangles(
            #     phone_screenshot,
            #     matched_click_region.get_original_match_rectangles())
            # Visualise.save_image(phone_screenshot, needle)

        except Exception as e:
            raise e

        x, y = matched_click_region.get_centres()[0]
        self._tap(x, y)

        time.sleep(config.TIMEOUTS.SLEEP_INTERVAL_AFTER_TAP)

    def pull(self, filepath, filename):
        self.device.sync.pull(filepath, filename)

    def _tap(self, x: int, y: int) -> None:
        self.device.click(x, y)

    def _swipe(self, sx: int, sy: int, ex: int, ey: int, duration: float = 1.0) -> None:
        self.device(sx, sy, ex, ey, duration)


if __name__ == "__main__":
    pass
    # d.click(418, 191)
