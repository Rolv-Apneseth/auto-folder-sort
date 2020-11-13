import os
import sys
import time
import logging
import watchdog

import assets.sorter


class CustomEventHandler(watchdog.FileSystemEventHandler):
    def __init__(self, sorter):
        self.sorter = sorter

    def on_modified(self, event):
        self.sort()
