import os
import shutil
from datetime import datetime

import constants


class Sorter:
    """Generates sorter objects which can sort all files in a given folder."""

    def __init__(
        self, folder: str, sort_type: str, earliest_year: int = datetime.today().year
    ) -> None:
        """
        folder: Folder that Sorter object will be sorting (absolute path must be given)

        sort_type: Either 'date' or 'file_type'

        earliest_year: Earliest year to create folders for if 'date' was given for sort_type

        Examples:
        >>> sorter = Sorter(os.path.dirname(__file__), 'file_type', 2019)
        >>> os.path.isdir(sorter.folder)
        True
        >>> os.path.isabs(sorter.folder)
        True
        >>> sorter.sort_type in ['file_type', 'date']
        True
        >>> 1920 <= sorter.earliest_year <= datetime.today().year
        True
        """

        self.folder = folder
        self.sort_type = sort_type
        self.earliest_year = earliest_year

        # Used in self.sort() to call the correct sort function based
        # on sort type
        self.s_dict: dict = {
            "file_type": self.sort_file,
            "date": self.sort_date
        }

        # List of all files/folders present in self.folder
        self.dir_files: list = os.listdir(self.folder)

    def assert_valid(self):
        """Returns whether the provided constructor arguments are valid.

        Examples:
        >>> sorter = Sorter(os.path.dirname(__file__), 'date', 2018)
        >>> sorter.assert_valid()
        True

        >>> sorter = Sorter(os.path.dirname(__file__), 'string', 2018)
        >>> sorter.assert_valid()
        False

        >>> sorter = Sorter(os.path.dirname(__file__), 'date', 2040)
        >>> sorter.assert_valid()
        False

        >>> sorter = Sorter(os.path.dirname(__file__), 'date', 1900)
        >>> sorter.assert_valid()
        False

        >>> sorter = Sorter(os.path.dirname(__file__), 'file_type', 1920)
        >>> sorter.assert_valid()
        True

        >>> sorter = Sorter("./", 'date')
        >>> sorter.assert_valid()
        False
        """
        self.today = datetime.today()
        self.year = self.today.year

        is_valid_folder = (
            type(self.folder) == str and
            os.path.isdir(self.folder) and
            os.path.isabs(self.folder)
        )

        is_valid_sort = self.sort_type in ["date", "file_type"]

        is_valid_earliest = (
            type(self.earliest_year) == int and
            1920 <= self.earliest_year <= self.year
        )

        return is_valid_folder and is_valid_sort and is_valid_earliest

    def update_dir_files(self) -> None:
        """Updates the list of files/folders present in self.folder.

        Examples:
        >>> sorter = Sorter(os.path.dirname(__file__), 'date', 2018)
        >>> dir_1 = sorter.dir_files
        >>> sorter.folder = os.path.dirname(os.path.dirname(__file__))
        >>> sorter.update_dir_files()
        >>> dir_1 == sorter.dir_files
        False

        >>> sorter = Sorter(os.path.dirname(__file__), 'file_type')
        >>> dir_1 = sorter.dir_files
        >>> sorter.update_dir_files()
        >>> dir_1 == sorter.dir_files
        True
        """

        self.dir_files: list = os.listdir(self.folder)

    def ensure_file_folders(self) -> None:
        """Ensures sorting folders for file types are present in self.folder."""

        self.update_dir_files()

        for file_type in constants.FILE_FOLDERS:
            if file_type not in self.dir_files:
                os.makedir(os.path.join(self.folder, file_type))

    def ensure_date_folders(self) -> None:
        """Ensures sorting folders for dates are present in self.folder.

        Folders will be structured in the layout: year -> month1, month2...

        A year folder will be generated for each year between
        self.earliest_year and the current year, inclusive.
        """

        self.update_dir_files()

        years: list = map(
            str, list(range(self.earliest_year, datetime.today().year + 1))
        )

        for year in years:
            if year not in self.dir_files:
                os.makedir(os.path.join(self.folder, year))

                for month in constants.MONTHS:
                    os.makedir(os.path.join(self.folder, year, month))

    def sort_file(self):
        pass

    def sort_date(self):
        pass

    def sort(self):
        """Calls appropriate sort function (file or date) based on self.sort_type"""

        self.s_dict[self.sort_type]()
