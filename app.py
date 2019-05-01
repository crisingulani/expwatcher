import sys
import time
import os
import logging

from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('exp-watcher.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s: %(name)s ~ %(levelname)s: %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)


class ExposureWatcher:
    def __init__(self, src_path):
        self.__src_path = src_path
        self.__event_handler = ExposureHandler()
        self.__event_observer = Observer()

    def run(self):
        self.start()
        try:
            while True: 
                global stop_thread 
                if stop_thread: 
                    break
                time.sleep(1)
        except Exception:
            logger.exception("File watcher interrupted")
        finally:
            self.stop()

    def start(self):
        self.__schedule()
        self.__event_observer.start()
        logger.info('File watcher started!')

    def stop(self):
        self.__event_observer.stop()
        self.__event_observer.join()
        logger.info('File watcher stoped!')

    def __schedule(self):
        self.__event_observer.schedule(
            self.__event_handler,
            self.__src_path,
            recursive=True
        )


class ExposureHandler(RegexMatchingEventHandler):
    # FILE_REGEX = [r".*\.fits$"]
    FILE_REGEX = [r".*"]

    def __init__(self):
        super().__init__(self.FILE_REGEX)

    def on_created(self, event):
        file_size = -1
        while file_size != os.path.getsize(event.src_path):
            file_size = os.path.getsize(event.src_path)
            time.sleep(2)

        self.process(event)

    def process(self, event):
        filename = os.path.basename(event.src_path)
        logger.info("Welcome {} exposure! :)".format(filename))

 
if __name__ == "__main__":
    import threading  
    src_path = sys.argv[1] if len(sys.argv) > 1 else '.'
    exp = ExposureWatcher(src_path)
    stop_thread = False
    t1 = threading.Thread(target=exp.run) 
    t1.start() 
    # simulate exposures arrival: it is time to copy the test
    # exposures in the 'src_path' directory.
    time.sleep(5) 
    stop_thread = True
    print('Bye')