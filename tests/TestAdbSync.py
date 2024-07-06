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


class TestPhonePull(unittest.TestCase):
    SAVE_FOLDER = "save files"
    SAVE_FOLDER_OUTPUT = "save file output"

    # @classmethod
    # def setUpClass(cls):
    #     remove_folder(TestPhonePull.SAVE_FOLDER)
    #     remove_folder(TestPhonePull.SAVE_FOLDER_OUTPUT)

    def test_file_pull_from_phone_to_desktop(self):
        remove_folder(TestPhonePull.SAVE_FOLDER)
        self.device = PhoneADB(config_override.config_settings["PHONE_NAME"])
        self.device.pull(
            config_override.config_settings["CITRA_SAVE_FOLDER_PHONE"], TestPhonePull.SAVE_FOLDER)

    def test_folder_backup(self):
        dt_string = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
        shutil.copytree(
            config_override.config_settings["CITRA_SAVE_FOLDER_PC"], os.path.join(Path(config_override.config_settings["CITRA_SAVE_FOLDER_PC"]).parent, dt_string))
        clear_folder(config_override.config_settings["CITRA_SAVE_FOLDER_PC"])
        shutil.copytree(TestPhonePull.SAVE_FOLDER,
                        config_override.config_settings["CITRA_SAVE_FOLDER_PC"], dirs_exist_ok=True)

    def test_push_desktop_citra_to_phone(self):
        self.device = PhoneADB(config_override.config_settings["PHONE_NAME"])

        remove_folder(TestPhonePull.SAVE_FOLDER_OUTPUT)
        shutil.copytree(config_override.config_settings["CITRA_SAVE_FOLDER_PC"],
                        TestPhonePull.SAVE_FOLDER_OUTPUT, dirs_exist_ok=True)

        files = [os.path.normpath(os.path.join(config_override.config_settings["CITRA_SAVE_FOLDER_PC"], file)) for file in os.listdir(
            config_override.config_settings["CITRA_SAVE_FOLDER_PC"])]

        for file in files:
            self.device.push(file,
                             config_override.config_settings["CITRA_SAVE_FOLDER_PHONE"])

        # def test_rename_folder(self):
        #     self.device = PhoneADB(config_override.config_settings["PHONE_NAME"])
        #     dt_string = os.path.join(Path(
        #         config_override.config_settings["CITRA_SAVE_FOLDER_PHONE"]).parent, datetime.now().strftime("%d-%m-%Y %H-%M-%S"))
        #     destination = str(PureWindowsPath(dt_string).as_posix())
        #     src = str(PurePosixPath(
        #         config_override.config_settings["CITRA_SAVE_FOLDER_PHONE"]))
        #     command = "su -c mv '{src}' '{destination}}'"
        #     value = self.device.shell(command)
        #     print()

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
