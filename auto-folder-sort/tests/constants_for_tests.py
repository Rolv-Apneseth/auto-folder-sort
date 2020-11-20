import os


### CONSTANTS ###
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))

# Used to test that sort_file function placed every sample
# file in exactly the right folder
TEST_FILE_FOLDERS = {
    "Folders & Archives": [
        "sample_folder",
        "sample.zip",
    ],
    "Executables": [
        "sample.run",
        "sample.exe",
        "sample.bat",
    ],
    "Documents & Data": [
        "sample.txt",
        "sample.ini",
    ],
    "Media": [
        "sample.mp4",
        "sample.jpeg",
    ],
    "Other": [],
}

# Used to check folder structure is unchanged before each test
SAMPLE_FILES = [
    "sample.run",
    "sample.mp4",
    "sample.exe",
    "sample_folder",
    "sample.txt",
    "sample.jpeg",
    "sample.zip",
    "sample.ini",
    "sample.bat",
]

MONTH_NUMBERS = {
    1: "(1) Jan",
    2: "(2) Feb",
    3: "(3) Mar",
    4: "(4) Apr",
    5: "(5) May",
    6: "(6) Jun",
    7: "(7) Jul",
    8: "(8) Aug",
    9: "(9) Sep",
    10: "(10) Oct",
    11: "(11) Nov",
    12: "(12) Dec"
}
