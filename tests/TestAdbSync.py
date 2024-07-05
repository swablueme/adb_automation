from unittest import mock
import config_override

from adb import *
import unittest
import image
import os
import shutil


class TestPhonePull(unittest.TestCase):
    def test_file_pull(self):
        SAVE_FOLDER = "save files"
        if os.path.exists(SAVE_FOLDER):
            shutil.rmtree(os.path.join(SAVE_FOLDER))
        self.device = PhoneADB("19241FDF6007JL")
        self.device.pull(
            "/sdcard/citra-emu/sdmc/Nintendo 3DS/00000000000000000000000000000000/00000000000000000000000000000000/title/00040000/000e5c00/data/00000001", SAVE_FOLDER)


if __name__ == '__main__':
    unittest.main(verbosity=2)
