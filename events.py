import os
import time
import datetime
from PIL import Image
from PIL.ImageOps import grayscale
from watchdog.events import RegexMatchingEventHandler

class ImagesEventHandler(RegexMatchingEventHandler):
    THUMBNAIL_SIZE = (128, 128)
    IMAGES_REGEX = [r".*[^_thumbnail]\.jpg$"]
    modimg = []

    def __init__(self):
        super().__init__(self.IMAGES_REGEX)

    def on_created(self, event):
        file_size = -1
        while file_size != os.path.getsize(event.src_path):
            file_size = os.path.getsize(event.src_path)
            time.sleep(1)

        #self.process(event)
        print("Created file {filename}".format(filename=event.src_path))

    def on_modified(self, event):
        file_size = -1
        while file_size != os.path.getsize(event.src_path):
            file_size = os.path.getsize(event.src_path)
            time.sleep(0.1)

        self.process(event)

    def process(self, event):
        print("File modified at {time}: {filename}".format(time=datetime.datetime.now(), filename=event.src_path))
        self.modimg.append(event.src_path)

    def clearArray(self):
        self.modimg.clear()