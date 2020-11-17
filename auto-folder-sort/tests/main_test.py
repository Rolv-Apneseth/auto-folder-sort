import logging
import os
import shutil
import unittest
from datetime import datetime

# Note that to run this test, you must execute:
# `python3 -m tests.main_test`
# from the main directory (where main.py is)
from main import Main, CustomEventHandler

# SAMPLE FILE PATHS
SAMPLE_PATH_1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Sample Files")
SAMPLE_PATH_2 = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "Sample Files (2)"
)


## Unit tests #
class TestMain(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()
