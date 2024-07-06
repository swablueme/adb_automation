from unittest import mock
import config_override

from adb import *
import unittest
import image
import os
import shutil
import config_override


class TestPhonePull(unittest.TestCase):
    def test_file_pull(self):
        SAVE_FOLDER = "save files"
        if os.path.exists(SAVE_FOLDER):
            shutil.rmtree(os.path.join(SAVE_FOLDER))
        self.device = PhoneADB(config_override.config_settings["PHONE_NAME"])
        self.device.pull(
            config_override.config_settings["CITRA_SAVE_FOLDER"], SAVE_FOLDER)


if __name__ == '__main__':
    unittest.main(verbosity=2)
