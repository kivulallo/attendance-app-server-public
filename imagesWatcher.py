import sys
import time
import ssl

from datetime import datetime
from watchdog.observers import Observer
from events import ImagesEventHandler
from face_training import Trainer
import paho.mqtt.client as mqtt
import printlog as pr

class ImagesWatcher:
    TRAIN_DELAY = 30
    mqc = mqtt.Client()
    context = ssl.create_default_context()

    def __init__(self, src_path):
        pr.pl("Watcher init")
        self.__src_path = src_path
        self.__event_handler = ImagesEventHandler()
        self.__event_observer = Observer()
        self.mqc.username_pw_set("username","password")
        self.mqc.connect("localhost")
        pr.pl("Watcher init done. MQTT connected")

    def run(self):
        self.start()
        seconds = 0
        pr.pl("Started file observer on "+str(self.__src_path))
        try:
            while True:
                self.mqc.loop_start()
                if seconds >= self.TRAIN_DELAY and len(self.__event_handler.modimg) > 0:
                    trainer = Trainer()
                    faces,ids = trainer.getImagesAndLabels(self.__src_path)
                    if(len(faces) > 0):
                        pr.pl("Found {0} files.".format(len(faces)))
                        trainer.train(faces,ids)
                        pr.pl("Publishing done message")
                        self.mqc.publish("cv/training", "training done at {0}".format(datetime.now()), 1)
                        pr.pl("Published")
                    else:
                        pr.pl("No faces found. Cancelling training.")
                    seconds = 0
                    self.__event_handler.clearArray()
                time.sleep(1)
                self.mqc.loop_stop()
                if seconds % 5 == 0:
                    pr.pl("Time elapsed {0} seconds".format(seconds))
                seconds += 1
        except KeyboardInterrupt:
            self.stop()

    def start(self):
        self.__schedule()
        self.__event_observer.start()

    def stop(self):
        self.__event_observer.stop()
        self.__event_observer.join()

    def __schedule(self):
        self.__event_observer.schedule(
            self.__event_handler,
            self.__src_path,
            recursive=True
        )

if __name__ == "__main__":
    src_path = sys.argv[1] if len(sys.argv) > 1 else './images'
    ImagesWatcher(src_path).run()
