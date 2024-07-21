from pathlib import Path
from unittest import mock
import config_override

from adb import *
import unittest
import image
import os
import shutil
import config_override
from datetime import datetime
from pathlib import PurePosixPath, PureWindowsPath
from utility import *
import binascii


class TestPhonePull(unittest.TestCase):
    SAVE_FOLDER = "save files"
    SAVE_FOLDER_OUTPUT = "save file output"

    def __init__(self, *args, **kwargs):
        super(TestPhonePull, self).__init__(*args, **kwargs)
        self.device = PhoneADB(config_override.config_settings["PHONE_NAME"])

    def test_file_pull_from_phone_to_desktop(self):
        for (phone, pc) in zip(config_override.config_settings["CITRA_SAVE_FOLDER_PHONE"], config_override.config_settings["CITRA_SAVE_FOLDER_PC"]):
            remove_folder(TestPhonePull.SAVE_FOLDER)
            self.device.pull(
                phone, TestPhonePull.SAVE_FOLDER)
            dt_string = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
            shutil.copytree(
                pc, os.path.join(Path(pc).parent, dt_string))
            clear_folder(pc)
            shutil.copytree(TestPhonePull.SAVE_FOLDER,
                            pc, dirs_exist_ok=True)

    def test_write300_playcoins(self):
        playcoins = bytes.fromhex(
            '00 4F 00 00 2C 01 00 00 00 00 00 00 00 00 00 00 E8 07 07 07')
        self.device.push(
            playcoins, config_override.config_settings["CITRA_PLAY_COINS_PHONE"])

    def test_push_desktop_citra_to_phone(self):
        for (phone, pc) in zip(config_override.config_settings["CITRA_SAVE_FOLDER_PHONE"], config_override.config_settings["CITRA_SAVE_FOLDER_PC"]):
            remove_folder(TestPhonePull.SAVE_FOLDER_OUTPUT)
            shutil.copytree(pc,
                            TestPhonePull.SAVE_FOLDER_OUTPUT, dirs_exist_ok=True)

            files = [os.path.normpath(os.path.join(pc, file)) for file in os.listdir(
                pc)]

            for file in files:
                self.device.push(file,
                                 phone)

    def push_saves(self):
        pass


def clear_folder(target_dir):
    with os.scandir(target_dir) as entries:
        for entry in entries:
            if entry.is_dir() and not entry.is_symlink():
                shutil.rmtree(entry.path)
            else:
                os.remove(entry.path)


if __name__ == '__main__':
    unittest.main(verbosity=2)
