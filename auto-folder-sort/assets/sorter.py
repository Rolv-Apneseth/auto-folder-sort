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

    def update_years(self) -> None:
        """Update the list of years that folders are to be generated for.

        Examples:
        >>> sorter = Sorter(os.path.dirname(__file__), 'date', 2018)
        >>> sorter.update_years()
        >>> type(sorter.years)
        <class 'list'>
        >>> years1 = list(map(str, list(range(2018, datetime.today().year + 1))))
        >>> sorter.years == years1
        True
        >>> sorter.earliest_year = 2017
        >>> sorter.update_years()
        >>> sorter.years == years1
        False

        >>> sorter = Sorter(os.path.dirname(__file__), 'date', 1969)
        >>> sorter.update_years()
        >>> type(sorter.years[0])
        <class 'str'>
        >>> years2 = list(range(1969, datetime.today().year + 1))
        >>> sorter.years == years2
        False
        >>> years3 = list(map(str, years2))
        >>> sorter.years == years3
        True
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
        self.update_years

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

            extension = os.path.splitext(item)[-1]

            for file_type, extensions in constants.FILE_FOLDERS.items():
                if extension in extensions:
                    old_path = os.path.join(self.folder, item)
                    new_path = os.path.join(self.folder, file_type, item)

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
            mod_local_time = time.ctime(mod_seconds)

            mod_month = mod_local_time[1]
            mod_year = mod_local_time[4]

            if int(mod_year) < self.earliest_year:
                print(
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
                raise IOError(
                    "\nOne of the following values given was invalid (False):"
                    f"\nFolder valid: {self.is_valid_folder}"
                    f"\nSort type valid: {self.is_valid_sort}"
                    f"\nEarliest year valid: {self.is_valid_earliest}"
                )
        except IOError as e:
            print(
                f"\nThere was an error while sorting files by {self.sort_type}:"
                f"\n{e.args}"
                "\nPlease check the log file for further information"
            )
            return False
        return True
