# auto-folder-sort

Allows automated sorting of a given folder or folders into organised subfolders

## What I learned

- File i/o with use of shutil
- Logging information into .log files
- Unit testing
- Use of the watchdog library to monitor a system folder for modifications

## Goals

- Learn how to use logs and how to make unit tests for my programs, both to make me a better programmer and get better at debugging programs.

- Automate a task using the watchdog library so a program could be left running indefinitely as a background process.

- Most importantly, I wanted to prove to myself that I am in fact improving my ability to code by comparing this project to my previous, similar project https://github.com/Rolv-Apneseth/file-sorter

## Installation

1. Requires python 3.6+ to run. Python can be installed from [here](https://www.python.org/downloads/)
2. To download, click on 'Code' to the top right, then download as a zip file. You can unzip using your preferred program.
   - You can also clone the repository using: `git clone https://github.com/Rolv-Apneseth/auto-folder-sort.git`
3. Install the requirements for the program.
   - In your terminal, navigate to the cloned directory and run: `python3 -m pip install -r requirements.txt`
4. To run the actual program, navigate further into the file-sorter folder and run: `python3 main.py`

## Usage

1. I strongly recommend running the built in tests before trying this on your personal files. To do this, navigate to auto-folder-sort and run `pyhton3 -m tests.main_test'.
   - All tests should pass with no issues. If ANY don't pass, please let me know and don't run the program on your folders as there is something wrong.
2. To set which folders you want sorted, you must edit the folders_to_track.txt file located in the same folder as main.py.
   - Each line will be read as 1 folder to track/sort and must have at least 2 space separated paramaeter provided
   - Required parameters: Folder path and sort type (can only be 'date' or 'file_type')
   - Optional parameter: Earliest year (for date sort, folders will be generated for years ranging from this value to the current year)
3. An example of an input file can be found in the examples folder.
4. With your folders_to_track.txt file correctly layed out, simply execute `python3 main.py' to begin sorting and tracking the specified folder(s).
   - This can be easily set to run on start up so folders will always remain sorted (very useful for, for example, the downloads folder)
