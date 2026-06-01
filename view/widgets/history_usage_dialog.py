"""
HistoryUsageDialog — Dialog lịch sử sử dụng gần đây.
"""
import time

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)

from view.ui_helpers import create_ui_footer
from view.widgets.base_dialog import FooterDialog


class HistoryUsageDialog(FooterDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(" Lịch sử sử dụng")
        self.setFixedSize(500, 400)
        self.setup_ui()
        create_ui_footer(self)

    def setup_ui(self):
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                               stop:0 #0f0f1a, stop:1 #1a1a2a);
                color: white;
            }
            QLabel {
                color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                               stop:0 #00ffaa, stop:1 #00ccff);
                font-size: 18px;
                font-weight: 300;
                text-align: center;
                padding: 15px;
            }
            QTextEdit {
                background: rgba(25, 25, 45, 180);
                border: 1px solid rgba(0, 255, 136, 40);
                border-radius: 10px;
                padding: 15px;
                color: white;
                font-size: 14px;
                font-family: 'Segoe UI';
            }
            QPushButton {
                background: rgba(0, 255, 136, 20);
                border: 1px solid rgba(0, 255, 136, 50);
                border-radius: 8px;
                padding: 8px 16px;
                color: #00ff88;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(0, 255, 136, 40);
            }
        """)

        layout = QVBoxLayout(self)

        title = QLabel(" Lịch sử sử dụng gần đây")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.history_text = QTextEdit()
        self.history_text.setReadOnly(True)

        now = time.strftime('%Y-%m-%d %H:%M:%S')
        history_data = [
            f"[{now}] Đăng nhập thành công",
            f"[{now}] Mở cài đặt hệ thống",
            f"[{now}] Sử dụng tính năng chat",
            f"[{now}] Truy cập admin panel",
        ]
        self.history_text.setText("\n".join(history_data))
        layout.addWidget(self.history_text)

        button_layout = QHBoxLayout()
        clear_btn = QPushButton("Xóa lịch sử")
        close_btn = QPushButton(" Đóng")
        button_layout.addWidget(clear_btn)
        button_layout.addWidget(close_btn)
        layout.addLayout(button_layout)

        clear_btn.clicked.connect(self.clear_history)
        close_btn.clicked.connect(self.reject)

    def clear_history(self):
        """Xóa toàn bộ nội dung lịch sử."""
        self.history_text.clear()
        QMessageBox.information(self, "Thành công", "Đã xóa lịch sử sử dụng!")
