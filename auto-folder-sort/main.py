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


# MAIN
class Main:
    def __init__(self):
        self.PICKLE_PATH = os.path.join(FILE_PATH, "assets", "observers.pkl")
        self.BACKUP_PATH = os.path.join(FILE_PATH, "assets", "backup_observers.pkl")

    # HELPER FUNCTIONS

    def pickle_exists(self) -> bool:
        return os.path.exists(self.PICKLE_PATH)

    def backup_exists(self) -> bool:
        return os.path.exists(self.BACKUP_PATH)

    def make_observer(self, folder, sort_type, earliest_year):
        """Generates an observer object, as well as the sorter and event handler for it."""

        sorter = Sorter(folder, sort_type, earliest_year)

        event_handler = CustomEventHandler(sorter)

        observer = Observer()
        observer.schedule(event_handler, folder, recursive=True)

        return observer

    def update_observers(self, folder, sort_type, earliest_year=datetime.today().year):
        pass

    def backup(self):
        if self.backup_exists():
            send2trash(self.BACKUP_PATH)

        if self.pickle_exists():
            os.rename(self.PICKLE_PATH, self.BACKUP_PATH)

    def load_observers(self):
        if self.pickle_exists():
            with open(self.PICKLE_PATH, "rb") as obs_pickle:
                self.observers = pickle.load(obs_pickle)
        elif self.backup_exists():
            with open(self.BACKUP_PATH, "rb") as obs_pickle:
                self.observers = pickle.load(obs_pickle)
        else:
            return False
        return True

    def startup(self):
        pass

    def main(self):
        pass
