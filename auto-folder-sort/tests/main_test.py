import logging
import os
import shutil
import unittest
from datetime import datetime

# Note that to run this test, you must execute:
# `python3 -m tests.main_test`
# from the main directory (where main.py is)
import main
from tests.constants_for_tests import SAMPLE_FILES, TEST_FILE_FOLDERS, TESTS_DIR


# CONSTANTS
SAMPLE_PATH_1 = os.path.join(TESTS_DIR, "Sample Files")
SAMPLE_PATH_2 = os.path.join(TESTS_DIR, "Sample Files (2)")

TEST_COMMANDS = os.path.join(TESTS_DIR, "test_folders_to_track.txt")


## Unit tests ##
class TestMain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(TEST_COMMANDS, "w") as new_commands:
            new_commands.write(f"{SAMPLE_PATH_1} file_type\n{SAMPLE_PATH_2} date 2018")

        # Changes where the sample_program object will read commands from
        main.COMMANDS_PATH = TEST_COMMANDS

    @classmethod
    def tearDownClass(cls):
        os.remove(TEST_COMMANDS)

        # Final assert at the end of all tests to make sure both
        # Sample Files folders are back to their original layout
        assert os.listdir(SAMPLE_PATH_1) == SAMPLE_FILES
        assert os.listdir(SAMPLE_PATH_2) == SAMPLE_FILES

    def setUp(self):
        self.sample_program = main.Main()

        # Stops test from running if either folder layout is incorrect
        assert os.listdir(SAMPLE_PATH_1) == SAMPLE_FILES
        assert os.listdir(SAMPLE_PATH_2) == SAMPLE_FILES

    def tearDown(self):
        del self.sample_program

    def test_event_handler(self):
        pass

    def test_init(self):
        pass

    def test_make_observer(self):
        pass

    def test_add_observer(self):
        pass

    def test_setup_observers(self):
        pass

    def test_run(self):
        pass


if __name__ == "__main__":
    unittest.main()
