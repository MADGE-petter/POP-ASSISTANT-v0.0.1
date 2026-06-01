"""
AudioDialog — Dialog cài đặt âm thanh.
"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QSpinBox,
    QVBoxLayout,
)

from view.ui_helpers import create_ui_footer
from view.widgets.base_dialog import FooterDialog


class AudioDialog(FooterDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Âm thanh")
        self.setFixedSize(400, 300)
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
            QSlider {
                min-height: 20px;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                               stop:0 rgba(243, 156, 18, 0.8), stop:1 rgba(230, 126, 34, 0.8));
                border: 2px solid rgba(243, 156, 18, 0.9);
                border-radius: 8px;
                color: #ffffff;
                font-size: 12px;
                font-weight: 700;
                padding: 8px 16px;
            }
        """)

        layout = QVBoxLayout(self)

        # Volume
        volume_layout = QHBoxLayout()
        volume_label = QLabel(" Âm lượng chính:")
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

    def get_audio_settings(self):
        """Trả về dict cài đặt âm thanh hiện tại."""
        return {
            'volume': self.volume_slider.value(),
            'speech_rate': self.rate_spin.value(),
        }
