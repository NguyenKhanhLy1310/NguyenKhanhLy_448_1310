import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
# Đã sửa đường dẫn import cho đúng cấu trúc thư mục ui/ của bạn
from ui.playfair_view import Ui_MainWindow  

class PlayfairClientApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Playfair Cipher Client")
        
        # Địa chỉ URL của Flask API (đang chạy ở port 5000)
        self.API_BASE_URL = "http://127.0.0.1:5000/api/playfair"
        
        # Kết nối sự kiện click nút với hàm xử lý logic
        self.btn_encrypt.clicked.connect(self.handle_encrypt)
        self.btn_decrypt.clicked.connect(self.handle_decrypt)

    def get_user_inputs(self):
        """Lấy dữ liệu từ giao diện và kiểm tra hợp lệ"""
        key = self.txt_key.text().strip()
        # Đã đổi thành .text() vì txt_input hiện tại là QLineEdit
        text = self.txt_input.text().strip()
        
        if not key or not text:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập đầy đủ cả Khóa (Key) và Văn bản!")
            return None, None
        return key, text

    def handle_encrypt(self):
        key, text = self.get_user_inputs()
        if not key:
            return
            
        try:
            # Gửi request POST dạng JSON lên Server mã hóa
            payload = {"text": text, "key": key}
            response = requests.post(f"{self.API_BASE_URL}/encrypt", json=payload)
            
            if response.status_code == 200:
                result_data = response.json()
                # Hiển thị kết quả mã hóa lên ô txt_output (QTextBrowser)
                self.txt_output.setPlainText(result_data.get("encrypted_text", ""))
            else:
                error_msg = response.json().get("error", "Lỗi không xác định")
                QMessageBox.critical(self, "Lỗi Server", f"Mã lỗi {response.status_code}: {error_msg}")
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Lỗi kết nối", "Không thể kết nối tới Server! Bạn đã bật file api.py chưa?")

    def handle_decrypt(self):
        key, text = self.get_user_inputs()
        if not key:
            return
            
        try:
            # Gửi request POST dạng JSON lên Server giải mã
            payload = {"text": text, "key": key}
            response = requests.post(f"{self.API_BASE_URL}/decrypt", json=payload)
            
            if response.status_code == 200:
                result_data = response.json()
                # Hiển thị kết quả giải mã lên ô txt_output (QTextBrowser)
                self.txt_output.setPlainText(result_data.get("decrypted_text", ""))
            else:
                error_msg = response.json().get("error", "Lỗi không xác định")
                QMessageBox.critical(self, "Lỗi Server", f"Mã lỗi {response.status_code}: {error_msg}")
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Lỗi kết nối", "Không thể kết nối tới Server! Bạn đã bật file api.py chưa?")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlayfairClientApp()
    window.show()
    sys.exit(app.exec_())