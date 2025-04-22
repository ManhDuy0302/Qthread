from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from queue import Queue, Empty
import time

class DisplayThread(QThread):
    __pixmap_ready = pyqtSignal(QPixmap)

    def __init__(self, process_queue: Queue):
        super().__init__()
        self.__thread_active = False
        self.__process_queue = process_queue

    def run(self):
        self.__thread_active = True
        while self.__thread_active:
            try:
                frame = self.__process_queue.get(timeout=1.0)
                height, width = frame.shape
                bytes_per_line = width
                q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
                pixmap = QPixmap.fromImage(q_image)
                self.__pixmap_ready.emit(pixmap)
                self.__process_queue.task_done()
            except Empty:
                continue
            time.sleep(0.01)

    def stop(self):
        self.__thread_active = False