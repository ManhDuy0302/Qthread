import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QTimer
from capture_thread import CaptureThread
from process_thread import ProcessThread
from display_thread import DisplayThread

class MainWindow(QMainWindow):
    def __init__(self, video_path: str):
        super().__init__()
        self.__video_path = video_path
        self.__setup_ui()

        # Khởi tạo các thread
        self.__capture_thread = CaptureThread(self.__video_path)
        self.__process_thread = ProcessThread(self.__capture_thread.buffer_cap)  # Chỉ truyền capture_queue
        self.__display_thread = DisplayThread(self.__process_thread.process_queue)  # Lấy process_queue qua property

        # Kết nối signal để hiển thị
        self.__display_thread._DisplayThread__pixmap_ready.connect(self.__update_display)

        # Timer để kiểm tra trạng thái thread
        self.__status_timer = QTimer()
        self.__status_timer.timeout.connect(self.__check_thread_status)
        self.__status_timer.setInterval(1000)  # Kiểm tra mỗi 1 giây
        self.__status_timer.start()

        # Bắt đầu các thread
        self.__capture_thread.start()
        self.__process_thread.start()
        self.__display_thread.start()

    def __setup_ui(self):
        self.setWindowTitle("Multi-Thread Video Processing with Queue")
        self.setGeometry(100, 100, 640, 480)

        # Tạo widget chính và layout
        self.__central_widget = QWidget()
        self.setCentralWidget(self.__central_widget)
        self.__layout = QVBoxLayout(self.__central_widget)

        # Label để hiển thị video
        self.__video_label = QLabel(self)
        self.__video_label.setAlignment(Qt.AlignCenter)
        self.__layout.addWidget(self.__video_label)

        # Label để hiển thị trạng thái các thread
        self.__capture_status = QLabel("Capture Thread: Not Running")
        self.__process_status = QLabel("Process Thread: Not Running")
        self.__display_status = QLabel("Display Thread: Not Running")
        self.__layout.addWidget(self.__capture_status)
        self.__layout.addWidget(self.__process_status)
        self.__layout.addWidget(self.__display_status)

    def __update_display(self, pixmap):
        self.__video_label.setPixmap(pixmap.scaled(
            self.__video_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        ))

    def __check_thread_status(self):
        capture_running = "Running" if self.__capture_thread.isRunning() else "Not Running"
        process_running = "Running" if self.__process_thread.isRunning() else "Not Running"
        display_running = "Running" if self.__display_thread.isRunning() else "Not Running"
        self.__capture_status.setText(f"Capture Thread: {capture_running}")
        self.__process_status.setText(f"Process Thread: {process_running}")
        self.__display_status.setText(f"Display Thread: {display_running}")

    def closeEvent(self, event):
        self.__capture_thread.stop()
        self.__process_thread.stop()
        self.__display_thread.stop()
        self.__capture_thread.wait()
        self.__process_thread.wait()
        self.__display_thread.wait()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    video_path = r"C:\Users\USER\Downloads\2\265501_tiny.mp4"
    window = MainWindow(video_path)
    window.show()
    sys.exit(app.exec_())