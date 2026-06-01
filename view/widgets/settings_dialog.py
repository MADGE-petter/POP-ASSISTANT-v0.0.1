"""
SettingsDialog — Dialog cài đặt hệ thống.
"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QSpinBox,
    QVBoxLayout,
)

from view.ui_helpers import create_ui_footer
from view.widgets.base_dialog import FooterDialog


class SettingsDialog(FooterDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tùy chỉnh hệ thống")
        self.setFixedSize(450, 400)
        self.setup_ui()
        create_ui_footer(self)

    def setup_ui(self):
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                               stop:0 #1a1f2a, stop:1 #2a2f3a);
                color: #e0e0e0;
            }
            QLabel {
                color: #e0e0e0;
                font-size: 12px;
                padding: 5px;
            }
            QCheckBox {
                color: #e0e0e0;
                font-size: 12px;
                padding: 5px;
            }
            QSpinBox {
                background: rgba(30, 35, 50, 90);
                border: 1px solid rgba(0, 255, 170, 40);
                border-radius: 6px;
                padding: 8px;
                color: #e0e0e0;
                font-size: 12px;
            }
            QSlider {
                min-height: 20px;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                               stop:0 rgba(39, 174, 96, 0.8), stop:1 rgba(34, 153, 84, 0.8));
                border: 2px solid rgba(39, 174, 96, 0.9);
                border-radius: 8px;
                color: #ffffff;
                font-size: 12px;
                font-weight: 700;
                padding: 8px 16px;
            }
        """)

        layout = QVBoxLayout(self)

        # Auto start assistant
        self.auto_start_cb = QCheckBox("Tự động khởi động assistant")
        self.auto_start_cb.setChecked(True)
        layout.addWidget(self.auto_start_cb)

        # Assistant delay
        delay_layout = QHBoxLayout()
        delay_label = QLabel("⏱Thời gian trễ (ms):")
        self.delay_spin = QSpinBox()
        self.delay_spin.setRange(100, 5000)
        self.delay_spin.setValue(1000)
        delay_layout.addWidget(delay_label)
        delay_layout.addWidget(self.delay_spin)
        delay_layout.addStretch()
        layout.addLayout(delay_layout)

        # Speech recognition
        self.speech_cb = QCheckBox(" Nhận dạng giọng nói")
        self.speech_cb.setChecked(True)
        layout.addWidget(self.speech_cb)

        # Text to speech
        self.tts_cb = QCheckBox(" Đọc văn bản thành giọng nói")
        self.tts_cb.setChecked(True)
        layout.addWidget(self.tts_cb)

        # Volume
        volume_layout = QHBoxLayout()
        volume_label = QLabel(" Âm lượng:")
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(80)
        volume_layout.addWidget(volume_label)
        volume_layout.addWidget(self.volume_slider)
        volume_layout.addStretch()
        layout.addLayout(volume_layout)

        # Speech rate
        rate_layout = QHBoxLayout()
        rate_label = QLabel(" Tốc độ nói:")
        self.rate_spin = QSpinBox()
        self.rate_spin.setRange(50, 200)
        self.rate_spin.setValue(100)
        rate_layout.addWidget(rate_label)
        rate_layout.addWidget(self.rate_spin)
        rate_layout.addStretch()
        layout.addLayout(rate_layout)

        layout.addStretch()

        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton(" Lưu")
        cancel_btn = QPushButton(" Hủy")
        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)

    def get_settings(self):
        """Trả về dict các giá trị cài đặt hiện tại."""
        return {
            'auto_start': self.auto_start_cb.isChecked(),
            'delay': self.delay_spin.value(),
            'speech_enabled': self.speech_cb.isChecked(),
            'tts_enabled': self.tts_cb.isChecked(),
            'volume': self.volume_slider.value(),
            'speech_rate': self.rate_spin.value(),
        }
