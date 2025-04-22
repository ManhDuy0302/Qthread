from PyQt5.QtCore import QThread
import cv2
from queue import Queue, Empty
import time

class ProcessThread(QThread):
    def __init__(self, capture_queue: Queue):
        super().__init__()
        self.__thread_active = False
        self.__capture_queue = capture_queue
        self.__process_queue = Queue(maxsize=10)  # Khởi tạo process_queue trong class

    @property
    def process_queue(self):
        return self.__process_queue

    def run(self):
        self.__thread_active = True
        while self.__thread_active:
            try:
                frame = self.__capture_queue.get(timeout=1.0)
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                if not self.__process_queue.full():
                    self.__process_queue.put(gray_frame)
                self.__capture_queue.task_done()
            except Empty:
                continue
            time.sleep(0.01)

    def stop(self):
        self.__thread_active = False