import logging
import os
import pickle
import sys
import time
from datetime import datetime

from send2trash import send2trash
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from assets.sorter import Sorter

FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)))


# EVENT HANDLER
class CustomEventHandler(FileSystemEventHandler):
    def __init__(self, sorter):
        self.sorter = sorter

    def on_modified(self, event):
        self.sorter.sort()


# MAIN CLASS
class Main:
    def __init__(self):
        self.observers = {}

        # Get commands from text file
        self.commands = []
        with open("folders_to_track.txt", "r") as txt:
            for line in txt.readlines():
                line = line.split()
                self.commands.append(line)

    # HELPER FUNCTIONS
    def make_observer(self, folder, sort_type, earliest_year):
        """Generates an observer object, as well as the sorter and event handler for it."""

        sorter = Sorter(folder, sort_type, earliest_year)

        event_handler = CustomEventHandler(sorter)

        observer = Observer()
        observer.schedule(event_handler, folder, recursive=True)

        return observer

    def add_observer(self, folder, sort_type, earliest_year=datetime.today().year):
        """Adds an observer object for a specific folder to self.observers."""

        new_observer = self.make_observer(folder, sort_type, earliest_year)
        self.observers[folder] = new_observer

    def get_observers(self):
        """Creates self.observers by instantiating observer objects
        based on self.commands."""

        for command in self.commands:
            if len(command) == 2:
                self.add_observer(command[0], command[1])
            elif len(command) == 3:
                self.add_observer(command[0], command[1], command[2])

    # MAIN
    def run(self):
        """Main method, keeps observers in self.observers running."""

        self.get_observers()

        for observer in self.observers.values():
            observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            for observer in self.observers.values():
                observer.stop()
                observer.join()


if __name__ == "__main__":
    program = Main()
    program.run()
