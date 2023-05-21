import tesserocr
from tesserocr import PyTessBaseAPI
import os


class TessarectConfigurationPrint:
    def __init__(self):
        print(tesserocr.tesseract_version())  # print tesseract-ocr version
        print(tesserocr.get_languages())  # print languages version


TessarectConfigurationPrint()
