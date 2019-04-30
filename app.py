import sys
import time
import os
import logging

from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler

logging.basicConfig(
    filename='expwatcher.log', filemode='w',
    format='%(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


class ExpWatcher:
    def __init__(self, src_path):
        self.__src_path = src_path
        self.__event_handler = ExpEventHandler()
        self.__event_observer = Observer()

    def run(self):
        self.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def start(self):
        self.__schedule()
        self.__event_observer.start()
        logger.info('Exposure Watcher started!')

    def stop(self):
        self.__event_observer.stop()
        logger.info('Exposure Watcher stoped!')
        self.__event_observer.join()

    def __schedule(self):
        self.__event_observer.schedule(
            self.__event_handler,
            self.__src_path,
            recursive=True
        )


class ExpEventHandler(RegexMatchingEventHandler):
    # EXP_REGEX = [r".*[^_thumbnail]\.jpg$"]
    EXP_REGEX = [r".*"]

    def __init__(self):
        super().__init__(self.EXP_REGEX)

    def on_created(self, event):
        self.process(event)

    def process(self, event):
        filename, ext = os.path.splitext(event.src_path)
        logger.info("Welcome {} file! :)".format(filename))

 
if __name__ == "__main__":
    src_path = sys.argv[1] if len(sys.argv) > 1 else '.'
    ExpWatcher(src_path).run()