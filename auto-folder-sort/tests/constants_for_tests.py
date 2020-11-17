### CONSTANTS ###
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
