#🧵 Giới thiệu về QThread và đa luồng trong PyQt5
Trong lập trình GUI, nếu một tác vụ chạy lâu trong main thread (GUI thread) thì giao diện sẽ bị "đơ", không thể tương tác cho đến khi tác vụ kết thúc. Để tránh điều này, ta sử dụng QThread – một lớp cung cấp khả năng chạy code ở một luồng riêng biệt mà không làm ảnh hưởng đến giao diện chính.

PyQt5 cung cấp hai cách sử dụng QThread:

Subclass QThread: Tạo một lớp con kế thừa từ QThread, override phương thức run().

Move to thread: Tạo một object bình thường rồi di chuyển nó sang QThread bằng moveToThread().

🔁 Cơ chế Signal-Slot trong PyQt5
Signal-Slot là cơ chế giao tiếp giữa các object trong Qt. Đặc biệt quan trọng trong đa luồng, giúp gửi dữ liệu hoặc thông báo từ thread phụ về GUI một cách an toàn (thread-safe).

Ví dụ cơ bản:

python
Sao chép
Chỉnh sửa
class Worker(QThread):
    progress = pyqtSignal(int)

    def run(self):
        for i in range(100):
            time.sleep(0.1)
            self.progress.emit(i)
Trong giao diện:

python
Sao chép
Chỉnh sửa
self.worker.progress.connect(self.updateProgressBar)
✅ Ưu điểm:
Giao tiếp an toàn giữa các luồng.

Tránh tương tác trực tiếp GUI từ thread phụ (có thể gây crash).

📦 Sử dụng Queue để truyền dữ liệu giữa các luồng
Python cung cấp queue.Queue() – một cấu trúc dữ liệu thread-safe (an toàn với đa luồng). Kết hợp với QThread, ta có thể để thread phụ thực hiện xử lý rồi đưa kết quả vào hàng đợi, và luồng chính sẽ đọc và xử lý tiếp.

Ví dụ:
Thread xử lý:

python
Sao chép
Chỉnh sửa
class Worker(QThread):
    def __init__(self, data_queue):
        super().__init__()
        self.queue = data_queue

    def run(self):
        for i in range(10):
            result = heavy_computation(i)
            self.queue.put(result)
Thread chính đọc queue:

python
Sao chép
Chỉnh sửa
def check_queue(self):
    while not self.queue.empty():
        data = self.queue.get()
        self.update_ui(data)
Bạn có thể dùng QTimer để kiểm tra queue định kỳ:

python
Sao chép
Chỉnh sửa
self.timer = QTimer()
self.timer.timeout.connect(self.check_queue)
self.timer.start(100)
🧩 Tích hợp với Qt Designer
Giao diện được thiết kế bằng Qt Designer (file .ui), sau đó load bằng uic.loadUi() hoặc chuyển sang .py bằng pyuic5.

python
Sao chép
Chỉnh sửa
from PyQt5 import uic
uic.loadUi("interface.ui", self)
Bạn có thể liên kết nút bấm với hành động tạo thread:

python
Sao chép
Chỉnh sửa
self.pushButtonStart.clicked.connect(self.start_thread)
