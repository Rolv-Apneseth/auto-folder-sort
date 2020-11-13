import datetime
import logging
import os
import sys
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from assets.sorter import Sorter


# EVENT HANDLER
class CustomEventHandler(FileSystemEventHandler):
    def __init__(self, sorter):
        self.sorter = sorter

    def on_modified(self, event):
        self.sorter.sort()


# HELPER FUNCTIONS
def make_observer(folder, sort_type, earliest_year=datetime.today().year):
    """Generates an observer object, as well as the sorter and event handler for it."""

    sorter = Sorter(folder, sort_type, earliest_year)

    event_handler = CustomEventHandler(sorter)

    observer = Observer()
    observer.schedule(event_handler, folder, recursive=True)

    return observer
