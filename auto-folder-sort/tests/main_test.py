import logging
import os
import shutil
import time
import unittest
from datetime import datetime

from watchdog.observers.inotify import InotifyObserver

# Note that to run this test, you must execute:
# `python3 -m tests.main_test`
# from the main directory (where main.py is)
import main
from assets.constants import MONTHS
from assets.sorter import Sorter
from tests.constants_for_tests import (
    MONTH_NUMBERS,
    SAMPLE_FILES,
    TEST_FILE_FOLDERS,
    TESTS_DIR,
)

# CONSTANTS
SAMPLE_PATH_1 = os.path.join(TESTS_DIR, "SampleFiles")
SAMPLE_PATH_2 = os.path.join(TESTS_DIR, "SampleFiles(2)")

TEST_COMMANDS = os.path.join(TESTS_DIR, "test_folders_to_track.txt")

LOG_PATH = os.path.join(os.path.dirname(TESTS_DIR), "logs", "main_test.log")

# LOG
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter("\n%(levelname)s\nTime: %(asctime)s\n%(message)s")
file_handler = logging.FileHandler(LOG_PATH)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


## Unit tests ##
class TestMain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(TEST_COMMANDS, "w") as new_commands:
            new_commands.write(f"{SAMPLE_PATH_2} file_type\n{SAMPLE_PATH_1} date 2018")

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
        self.sample_sorter = Sorter(SAMPLE_PATH_1, "date", 2018)
        self.sample_file_type_sorter = Sorter(SAMPLE_PATH_2, "file_type")

        self.temp_dir = None
        self.temp_dirs = {}
        self.temp_month_dir = None
        self.temp_year_dir = None
        self.temp_path = None
        self.temp_month_path = None
        self.temp_year_path = None
        self.event_handler = None
        self.test_commands = None
        self.test_observer = None
        self.new_file_1 = None
        self.new_file_2 = None

        # Stops test from running if either folder layout is incorrect
        assert os.listdir(SAMPLE_PATH_1) == SAMPLE_FILES
        assert os.listdir(SAMPLE_PATH_2) == SAMPLE_FILES

    def tearDown(self):
        del self.sample_program
        del self.sample_sorter
        del self.sample_file_type_sorter

    # HELPER FUNCTIONS

    def undo_date_sort(self):
        """Undoes folders generated by sort_date method from a Sorter object
        and moves files to their original folder.

        Copied but slightly modified from sorter_test.py.
        """

        for year in self.sample_sorter.years:
            self.temp_year_path = os.path.join(self.sample_sorter.folder, year)
            self.temp_year_dir = os.listdir(self.temp_year_path)

            for month in self.temp_year_dir:
                self.temp_month_path = os.path.join(self.temp_year_path, month)
                self.temp_month_dir = os.listdir(self.temp_month_path)

                # All sample files created in November 2020
                if year == "2020" and month == "(11) Nov":
                    self.temp_dir = self.temp_month_dir

                for item in self.temp_month_dir:
                    shutil.move(
                        os.path.join(self.temp_month_path, item),
                        os.path.join(self.sample_sorter.folder, item),
                    )
                os.rmdir(self.temp_month_path)
            os.rmdir(self.temp_year_path)

    def undo_file_sort(self):
        """Undoes folders generated by sort_file method from a Sorter object
        and moves files to their original folder.

        Copied but slightly modified from sorter_test.py.
        """

        for file_type in TEST_FILE_FOLDERS:
            self.temp_path = os.path.join(
                self.sample_file_type_sorter.folder, file_type
            )
            self.temp_dir = os.listdir(self.temp_path)

            self.temp_dirs[file_type] = self.temp_dir

            for item in self.temp_dir:
                shutil.move(
                    os.path.join(self.temp_path, item),
                    os.path.join(self.sample_file_type_sorter.folder, item),
                )
            os.rmdir(self.temp_path)

    # TESTS

    def test_event_handler_init(self):
        # Note that the event_handler's on_modified method is tested while
        # observers are being tested so only it's constructor method can be
        # tested separately
        self.event_handler = main.CustomEventHandler(self.sample_sorter)

        self.undo_date_sort()
        self.assertEqual(self.temp_dir, SAMPLE_FILES)

    def test_init(self):

        with open(TEST_COMMANDS, "r") as text:
            self.test_commands = [line.split() for line in text.readlines()]

        self.assertEqual(self.sample_program.commands, self.test_commands)

    def test_make_observer(self):
        # Parameters must be the same as for sample_sorter so
        # undo_date_sort functions as normal
        self.test_observer = self.sample_program.make_observer(
            SAMPLE_PATH_1, "date", 2018
        )
        self.sample_sorter.update_years()

        self.undo_date_sort()
        self.assertEqual(self.temp_dir, SAMPLE_FILES)

        self.assertIsInstance(self.test_observer, InotifyObserver)

        self.assertRaises(
            IOError, lambda: self.sample_program.make_observer("./", "date", 2018)
        )
        self.assertRaises(
            IOError,
            lambda: self.sample_program.make_observer(SAMPLE_PATH_1, "string", 2018),
        )
        self.assertRaises(
            IOError,
            lambda: self.sample_program.make_observer(SAMPLE_PATH_1, "date", "2018"),
        )

    def test_add_observer(self):
        # Parameters must be the same as for sample_sorter so
        # undo_date_sort functions as normal
        self.sample_program.add_observer(SAMPLE_PATH_1, "date", 2018)
        self.sample_sorter.update_years()
        self.undo_date_sort()
        self.assertEqual(self.temp_dir, SAMPLE_FILES)

        self.sample_program.add_observer(SAMPLE_PATH_2, "date", 2018)
        # Change path for sample_sorter so undo_date_sort works
        self.sample_sorter.folder = SAMPLE_PATH_2
        self.undo_date_sort()
        self.assertEqual(self.temp_dir, SAMPLE_FILES)

        self.assertEqual(len(self.sample_program.observers), 2)
        self.assertIsInstance(
            self.sample_program.observers[SAMPLE_PATH_1], InotifyObserver
        )
        self.assertIsInstance(
            self.sample_program.observers[SAMPLE_PATH_2], InotifyObserver
        )

        # Negative
        for _ in range(100):
            self.sample_program.add_observer(SAMPLE_PATH_1, "date", 2018)
        self.assertEqual(len(self.sample_program.observers), 2)

    def test_setup_observers(self):
        self.sample_program.setup_observers()
        self.sample_sorter.update_years()

        self.undo_date_sort()
        self.assertEqual(self.temp_dir, SAMPLE_FILES)

        self.undo_file_sort()
        for file_type in self.temp_dirs:
            self.assertEqual(self.temp_dirs[file_type], TEST_FILE_FOLDERS[file_type])

        self.assertEqual(len(self.sample_program.observers), 2)
        for observer in self.sample_program.observers.values():
            self.assertIsInstance(observer, InotifyObserver)

    def test_observer_objects(self):
        # START OBSERVERS
        self.sample_program.setup_observers()
        self.sample_sorter.update_years()

        for observer in self.sample_program.observers.values():
            observer.start()

        # NEW FILES
        self.new_file_1 = os.path.join(SAMPLE_PATH_1, "new_file.txt")
        self.new_file_2 = os.path.join(SAMPLE_PATH_2, "new_file.txt")

        for new_file in (self.new_file_1, self.new_file_2):
            with open(new_file, "w") as text:
                text.write("")

        # STOP OBSERVERS
        time.sleep(0.5)  # so observers have time to detect modification
        self.sample_program.stop_observers()

        # UNDO AND VALIDATE DATE SORT
        # First, check new_file.txt was in fact sorted correctly
        self.temp_path = os.path.join(
            SAMPLE_PATH_1,
            str(datetime.today().year),
            MONTH_NUMBERS[datetime.today().month],
        )
        self.temp_dir = os.listdir(self.temp_path)
        self.assertTrue("new_file.txt" in self.temp_dir)

        self.undo_date_sort()  # Undo folders

        # new_file should be in the same folder as other sample files while
        # this test is run within the same month and year as the sample files
        # were created in
        if datetime.today().year == 2020 and datetime.today().month == 11:
            self.assertEqual(
                sorted(self.temp_dir), sorted(SAMPLE_FILES + ["new_file.txt"])
            )
        else:
            self.assertEqual(self.temp_dir, SAMPLE_FILES)

        # UNDO AND VALIDATE FILE TYPE SORT
        self.undo_file_sort()
        for file_type in self.temp_dirs:
            if file_type != "Documents & Data":
                self.assertEqual(
                    self.temp_dirs[file_type], TEST_FILE_FOLDERS[file_type]
                )
            else:
                self.assertEqual(
                    sorted(self.temp_dirs[file_type]),
                    sorted(TEST_FILE_FOLDERS[file_type] + ["new_file.txt"]),
                )

        # DELETE NEW FILES
        os.remove(self.new_file_1)
        os.remove(self.new_file_2)


if __name__ == "__main__":
    unittest.main()
