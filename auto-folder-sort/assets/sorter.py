import logging
import os
import shutil
import time
from datetime import datetime

# If being run directly or by runnint sorter_test.py, assets.constants
# will fail so use import constants instead
try:
    import assets.constants as constants
except ImportError:
    import constants

# Log
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

formatter = logging.Formatter(
    "\n%(levelname)s\nTime: %(asctime)s\nFile: %(filename)s:\n%(message)s"
)
log_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "logs", "sorter.log"
)

file_handler = logging.FileHandler(log_path)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


class Sorter:
    """Generates sorter objects which can sort all files in a given folder."""

    def __init__(
        self, folder: str, sort_type: str, earliest_year: int = datetime.today().year
    ) -> None:
        """
        folder: Folder that Sorter object will be sorting (absolute path must be given)

        sort_type: Either 'date' or 'file_type'

        earliest_year: Earliest year to create folders for if 'date'
                       was given for sort_type
        """

        self.folder = folder
        self.sort_type = sort_type
        self.earliest_year = earliest_year

        # Used in self.sort() to call the correct functions
        # based on sort type
        self.s_dict: dict = {
            "file_type": [self.ensure_file_folders, self.sort_file],
            "date": [self.ensure_date_folders, self.sort_date],
        }

        logger.info(
            f"Created Sorter object for: {self.folder}"
            f"\nSorting by: {self.sort_type}"
        )
        logger.debug(
            "Other attributes:" f"\nearliest year: {self.earliest_year}",
        )

    def assert_valid(self) -> bool:
        """Returns whether the provided constructor arguments are valid."""

        self.today = datetime.today()
        self.year = self.today.year

        self.is_valid_folder = (
            type(self.folder) == str
            and os.path.isdir(self.folder)
            and os.path.isabs(self.folder)
        )

        self.is_valid_sort = self.sort_type in ["date", "file_type"]

        self.is_valid_earliest = (
            type(self.earliest_year) == int and 1920 <= self.earliest_year <= self.year
        )

        return self.is_valid_folder and self.is_valid_sort and self.is_valid_earliest

    def update_dir_files(self) -> None:
        """Updates the list of files/folders present in self.folder."""

        self.dir_files: list = os.listdir(self.folder)

    def update_years(self) -> None:
        """Update the list of years that folders are to be generated for.

        If the list does not currently exist, then  it creates it.
        """

        self.years: list = list(
            map(str, list(range(self.earliest_year, datetime.today().year + 1)))
        )

    def ensure_file_folders(self) -> None:
        """Ensures sorting folders for file types are present in self.folder."""

        self.update_dir_files()

        for file_type in constants.FILE_FOLDERS:
            if file_type not in self.dir_files:
                os.mkdir(os.path.join(self.folder, file_type))

    def ensure_date_folders(self) -> None:
        """Ensures sorting folders for dates are present in self.folder.

        Folders will be structured in the layout: year -> month1, month2...

        A year folder will be generated for each year between
        self.earliest_year and the current year, inclusive.
        """

        self.update_dir_files()
        self.update_years()

        for year in self.years:
            if year not in self.dir_files:
                os.mkdir(os.path.join(self.folder, year))

                for month in constants.MONTHS:
                    os.mkdir(
                        os.path.join(
                            self.folder, year, f"{constants.MONTHS[month]} {month}"
                        )
                    )

    def sort_file(self):
        """Sorts self.folder by file type."""

        self.update_dir_files()

        for item in self.dir_files:
            # Don't sort the generated sort folders
            if item in constants.FILE_FOLDERS:
                continue

            old_path = os.path.join(self.folder, item)

            if os.path.isdir(old_path):
                new_path = os.path.join(self.folder, "Folders & Archives", item)

            else:
                extension = os.path.splitext(item)[-1][1:]

                for file_type in constants.FILE_FOLDERS:
                    if extension in constants.FILE_FOLDERS[file_type]:
                        new_path = os.path.join(self.folder, file_type, item)
                        break
                else:
                    new_path = os.path.join(self.folder, "Other", item)

            logger.info(f"Moving {old_path} to {new_path}")

            shutil.move(old_path, new_path)

    def sort_date(self):
        """Sorts self.folder by date of last modification."""

        self.update_dir_files()

        for item in self.dir_files:
            # Don't sort the generated sort folders
            if item in self.years:
                continue

            old_path = os.path.join(self.folder, item)

            # Time since modification to file/folder in seconds are
            # converted to local time when file was modified
            mod_seconds = os.path.getmtime(old_path)
            mod_local_time = time.ctime(mod_seconds).split()

            mod_month = mod_local_time[1]
            mod_year = mod_local_time[-1]

            if int(mod_year) < self.earliest_year:
                logger.warning(
                    f"\n{item} was last modified {mod_local_time}"
                    "\nThis is earlier than the earliest given year of "
                    f"{self.earliest}, so the file was skipped while sorting."
                )
                continue

            new_path = os.path.join(
                self.folder,
                mod_year,
                f"{constants.MONTHS[mod_month]} {mod_month}",
                item,
            )

            logger.info(f"Moving {old_path} to {new_path}")

            shutil.move(old_path, new_path)

    def sort(self):
        """Calls appropriate sort function (file or date) based on self.sort_type"""

        try:
            if self.assert_valid():
                # Executes respective ensure function then
                # respective sort function
                self.s_dict[self.sort_type][0]()
                self.s_dict[self.sort_type][1]()
            else:
                raise IOError
        except IOError as e:
            print(
                f"\nThere was an error while sorting files by {self.sort_type}:"
                f"\n{e.args}\n"
                "\nPlease check the log file for further information"
            )

            logger.exception(
                f"Error while sorting by {self.sort_type}"
                f"Sorter is valid: {self.assert_valid()}"
                f"\nCheck the following attributes of sorter object {self}"
                f"\nFolder valid: {self.is_valid_folder}"
                f"\nSort type valid: {self.is_valid_sort}"
                f"\nEarliest year valid: {self.is_valid_earliest}"
                "\nAlso make sure that the current folder is not being changed by"
                f"\nanother program. Current folder: {self.folder}"
            )

            logger.debug(
                f"Other sorter object {self} attributes:"
                f"\nearliest_year = {self.earliest_year}"
                f"\ntoday = {self.today}"
            )

            return False
        return True
