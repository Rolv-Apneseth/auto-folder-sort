import os
import unittest

from sorter import Sorter


class TestSorter(unittest.TestCase):
    def setUp(self):

        self.sorter1 = Sorter(os.path.dirname(
            os.path.abspath(__file__)), "date", 2018)
        self.sorter2 = Sorter(os.path.dirname(
            os.path.abspath(__file__)), "file_type")

    def test_init(self):
        self.assertEqual(
            self.sorter1.folder, os.path.dirname(os.path.abspath(__file__))
        )
        self.assertEqual(self.sorter2.sort_type, "file_type")
        self.assertEqual(self.sorter1.earliest_year, 2018)

    def test_assert_valid(self):
        self.assertTrue(self.sorter1.assert_valid())
        self.assertTrue(self.sorter2.assert_valid())

        # Sort type
        sorter_temp = Sorter(os.path.dirname(
            os.path.abspath(__file__)), "string", 2018)
        self.assertFalse(sorter_temp.assert_valid())

        # Earliest year
        sorter_temp.sort_type = "date"
        sorter_temp.earliest_year = 1900
        self.assertFalse(sorter_temp.assert_valid())
        sorter_temp.earliest_year = 2040
        self.assertFalse(sorter_temp.assert_valid())
        sorter_temp.earliest_year = "2018"
        self.assertFalse(sorter_temp.assert_valid())

        # Folder
        sorter_temp = Sorter("./", "date")
        self.assertFalse(sorter_temp.assert_valid())
        sorter_temp.folder = "folder"
        self.assertFalse(sorter_temp.assert_valid())

    def test_update_dir_files(self):
        self.sorter1.update_dir_files()
        dir1 = self.sorter1.dir_files
        self.sorter2.update_dir_files()
        dir2 = self.sorter2.dir_files
        self.assertTrue(dir1 == dir2)

        self.sorter1.folder = os.path.dirname(self.sorter1.folder)
        self.sorter2.folder = os.path.dirname(self.sorter2.folder)
        self.sorter1.update_dir_files()
        self.sorter2.update_dir_files()
        self.assertFalse(dir1 == self.sorter1.dir_files)
        self.assertTrue(self.sorter1.dir_files == self.sorter2.dir_files)


if __name__ == "__main__":
    unittest.main()
