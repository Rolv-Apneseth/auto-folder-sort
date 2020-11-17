import logging
import os
import shutil
import unittest
from datetime import datetime

# Note that to run this test, you must execute:
# `python3 -m tests.main_test`
# from the main directory (where main.py is)
from main import Main, CustomEventHandler
from tests.constants_for_tests import SAMPLE_FILES, TEST_FILE_FOLDERS


# SAMPLE FILE PATHS
SAMPLE_PATH_1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Sample Files")
SAMPLE_PATH_2 = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "Sample Files (2)"
)


## Unit tests #
class TestMain(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        # Final assert at the end of all tests to make sure both
        # Sample Files folders are back to their original layout
        assert os.listdir(SAMPLE_PATH_1) == SAMPLE_FILES
        assert os.listdir(SAMPLE_PATH_2) == SAMPLE_FILES

    def setUp(self):

        # Stops test from running if either folder layout is incorrect
        assert os.listdir(SAMPLE_PATH_1) == SAMPLE_FILES
        assert os.listdir(SAMPLE_PATH_2) == SAMPLE_FILES


if __name__ == "__main__":
    unittest.main()
