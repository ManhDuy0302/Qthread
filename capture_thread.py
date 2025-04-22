from PyQt5.QtCore import QThread
import cv2
import time
from queue import Queue

class CaptureThread(QThread):
    def __init__(self, video_path: str):
        super().__init__()
        self.__thread_active = False
        self.__buffer_cap = Queue()
        self.__max_buffer_size = 10
        self.__video_path = video_path
        self.__cap = None
        self.__fps = 12.0
        self.__previous_path = self.__video_path

    def __setup_cap(self):
        self.__cap = cv2.VideoCapture(self.__video_path)
        if self.__cap.isOpened():
            self.__fps = self.__cap.get(cv2.CAP_PROP_FPS) or 12.0
        else:
            print(f"Error: Cannot open video file {self.__video_path}")

    def __reconnect(self):
        self.__setup_cap()
        print("Reconnecting to video...")

    @property
    def buffer_cap(self):
        return self.__buffer_cap

    def run(self):
        self.__thread_active = True
        self.__setup_cap()
        if not self.__cap.isOpened():
            return

        while self.__thread_active:
            ret, frame = self.__cap.read()

            if not ret:
                self.__reconnect()
                print("Reconnect attempt")
                time.sleep(3)
                continue

            '''if self.__previous_path != self.__video_path:
                self.__setup_cap()
                print("Previous path:", self.__previous_path)
                print("New video path:", self.__video_path)
                self.__previous_path = self.__video_path
                continue'''

            if self.__buffer_cap.qsize() < self.__max_buffer_size:
                self.__buffer_cap.put(frame)

            if "mp4" in self.__video_path.lower():
                time.sleep(1.0 / self.__fps)
            else:
                time.sleep(0.001)


    def stop(self):
        self.__thread_active = False