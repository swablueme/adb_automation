
from unittest import mock
import config_override

from adb import *
import unittest
import image


class CONFIGURATION:
    IMAGE_MATCHING_TEMPLATE_FOLDER = "C:\\Users\\Destiny Chan\\Documents\\Actual Scripts\\opencv_cached_bot\\tests\\images\\FEH"


class TestPhoneClick(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestPhoneClick, self).__init__(*args, **kwargs)

    def testClick(self):
        device = PhoneADB()
        self.app_icon = ImageFile("app_icon.png")

    @mock.patch("adb.config.TIMEOUTS.TIMEOUT_UNTIL_IMAGE_FIND_OPERATION_CANCELLED", 1)
    def testTimeout(self):
        device = PhoneADB()
        self.assertRaises(TimeoutError,
                          device.tap_image, "unfindable_image.png")

    @timer
    def execute_close(self, device):
        device.tap_image("close.png")

    def testScrenshot(self):
        device = PhoneADB()
        device.screenshot().view()

    @mock.patch("image.config.CONFIGURATION.IMAGE_MATCHING_TEMPLATE_FOLDER", CONFIGURATION.IMAGE_MATCHING_TEMPLATE_FOLDER)
    def testForgingBonds(self):
        device = PhoneADB()

        while True:
            device.tap_image("FB@difficulty.png")
            device.tap_image("FB@fight.png")

            try:
                device.tap_image("FB@stamina.png", timeout=2)
                device.tap_image("FB@close1.png", timeout=2)
            except:
                break

            device.tap_image("FB@fight2.png")
            time.sleep(2)
            device.tap_image("FB@auto.png")
            device.tap_image("FB@autoconfirm.png")
            device.tap_image("FB@stageclear.png")
            while True:
                try:
                    device.tap_image("FB@close1.png", timeout=2)
                except:
                    break
            while True:
                try:
                    device.tap_image("FB@skip.png", timeout=3)
                except:
                    break

            while True:
                try:
                    device.tap_image("FB@close1.png", timeout=3)
                except:
                    break

    @mock.patch("image.config.CONFIGURATION.IMAGE_MATCHING_TEMPLATE_FOLDER", CONFIGURATION.IMAGE_MATCHING_TEMPLATE_FOLDER)
    def testTrainingTower(self):
        device = PhoneADB()

        while True:
            device.tap_image("training_tower.png")
            device.tap_image("fight_tt.png")
            device.wait_for_image("inbattle.png")
            device.tap_image("fight_battle.png")
            time.sleep(3)
            device.tap_image("autobattle.png")
            device.tap_image("autobattle_confirm.png")
            device.tap_image("stageclear.png", timeout=30)
            while True:
                try:
                    self.execute_close(device)
                except:
                    break


if __name__ == '__main__':
    unittest.main(verbosity=3)
