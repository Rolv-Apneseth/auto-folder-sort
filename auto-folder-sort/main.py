import logging
import os
import time
from datetime import datetime

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from assets.sorter import Sorter

# CONSTANTS
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(DIR_PATH, "logs", "main.log")
COMMANDS_PATH = os.path.join(DIR_PATH, "folders_to_track.txt")

# LOG
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

formatter = logging.Formatter("\n%(levelname)s\nTime: %(asctime)s\n%(message)s")
file_handler = logging.FileHandler(LOG_PATH)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


# EVENT HANDLER CLASS
class CustomEventHandler(FileSystemEventHandler):
    def __init__(self, sorter):
        self.sorter = sorter

        # Run sorter for the first time, in case folder has not
        # been sorted before. Returns True if sort was successful
        self.was_sorted = self.sorter.sort()

        if not self.was_sorted:
            logger.warning(
                f"\nSorter for {self.sorter.folder} was not able to sort successfully."
                f"\nSorter valid: {self.sorter.assert_valid()}"
            )

            raise IOError

    def on_modified(self, event):
        logger.info(f"Folder {event.src_path} modified")

        self.was_sorted = self.sorter.sort()

        if not self.was_sorted:
            logger.warning(
                f"\nSorter for {self.sorter.folder} was not able to sort successfully."
                f"\nSorter valid: {self.sorter.assert_valid()}"
            )


# MAIN CLASS
class Main:
    def __init__(self):
        self.observers = {}

        # Get commands from text file
        with open(COMMANDS_PATH, "r") as txt:
            # Splits each line at '|' and strips each item of trailing whitespace
            self.commands = [
                list(map(str.strip, line.split("|"))) for line in txt.readlines()
            ]

        logger.debug(f"Commands read from text file: {self.commands}")

        # Validate commands
        for command in self.commands:
            # Note that wheteher commands are correct folder paths,
            # valid year etc. are checked within the Sorter class
            # and return an error there

            if not 1 < len(command) < 4:
                logger.error(
                    f"\nA provided command in {COMMANDS_PATH} has less than 2 or more than 3 parameters."
                    f"\nFull command/line in file: {command}"
                )
            elif command[1] not in ("date", "file_type"):
                logger.error(
                    f"\nA provided command in {COMMANDS_PATH} has given an"
                    f"\ninvalid sort type. Sort type given: {command[1]}"
                    f"\nFull command/line in file: {command}"
                )
            else:
                continue

            raise ValueError(f"Please fix commands given at {COMMANDS_PATH}")

    # HELPER METHODS
    def make_observer(self, folder, sort_type, earliest_year):
        """Generates an observer object, as well as the sorter and event handler for it."""

        sorter = Sorter(folder, sort_type, earliest_year)

        event_handler = CustomEventHandler(sorter)

        observer = Observer()
        observer.schedule(event_handler, folder, recursive=True)

        return observer

    def add_observer(self, folder, sort_type, earliest_year=datetime.today().year):
        """Adds an observer object for a specific folder to self.observers."""

        if folder not in self.observers:
            new_observer = self.make_observer(folder, sort_type, earliest_year)
            self.observers[folder] = new_observer

            logger.info(
                f"\nObserver created for {folder} and added to self.observers."
                f"\nCurrent state of self.observers: {self.observers}"
            )
        else:
            logger.warning(
                "\nObserver could not be created as there is already an observer"
                f"\nmonitoring the folder: {folder}"
            )

    def setup_observers(self):
        """Creates self.observers by instantiating observer objects
        based on self.commands."""

        for command in self.commands:
            if len(command) == 2:
                self.add_observer(command[0], command[1])
            elif len(command) == 3:
                self.add_observer(command[0], command[1], int(command[2]))

    def stop_observers(self):
        """Stops all observers in self.observers from running. Used before program
        shuts down"""

        for observer in self.observers.values():
            observer.stop()
            observer.join()

    # MAIN
    def run(self):
        """Main method, keeps observers in self.observers running."""

        self.setup_observers()

        for observer in self.observers.values():
            observer.start()

        try:
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            logger.debug("Keyboard interrupt detected. Observers have been stopped.")

            self.stop_observers()

        except IOError:
            self.stop_observers()

            logger.exception("IOError detected. Observers have been stopped.")


if __name__ == "__main__":
    program = Main()
    program.run()
