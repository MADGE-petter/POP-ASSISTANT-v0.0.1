import time

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSlider,
    QSpinBox,
    QVBoxLayout,
)

from view.ui_helpers import create_ui_footer, position_ui_footer


class FooterDialog(QDialog):
    def resizeEvent(self, event):
        super().resizeEvent(event)
        position_ui_footer(self)


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
        
        # Handle buttons
        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
    
    def get_settings(self):
        """Get current settings values"""
        return {
            'auto_start': self.auto_start_cb.isChecked(),
            'delay': self.delay_spin.value(),
            'speech_enabled': self.speech_cb.isChecked(),
            'tts_enabled': self.tts_cb.isChecked(),
            'volume': self.volume_slider.value(),
            'speech_rate': self.rate_spin.value()
        }


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
        
        # Handle buttons
        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
    
    def get_audio_settings(self):
        """Get audio settings values"""
        return {
            'volume': self.volume_slider.value(),
            'speech_rate': self.rate_spin.value()
        }


class PersonalInfoDialog(FooterDialog):
    def __init__(self, user_name, sql_service, parent=None):
        super().__init__(parent)
        self.user_name = user_name
        self.sql_service = sql_service
        self.setWindowTitle(" Thông tin cá nhân")
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
            QDialog QLabel {
                color: white;
                font-size: 14px;
            }
            QDialog QPushButton {
                background: rgba(0, 255, 136, 20);
                border: 1px solid rgba(0, 255, 136, 50);
                border-radius: 6px;
                padding: 8px 16px;
                color: #00ff88;
                font-weight: bold;
                min-width: 80px;
            }
            QDialog QPushButton:hover {
                background: rgba(0, 255, 136, 40);
            }
        """)
        
        layout = QVBoxLayout(self)
        
        # Get user statistics via service
        try:
            stats = self.sql_service.get_user_stats(self.user_name)
            if stats:
                info_text = f"""Tên người dùng: {self.user_name}

Thống kê sử dụng:
• Tổng số cuộc trò chuyện: {stats['total_conversations']}
• Số ngày sử dụng: {stats['total_days']}
• Số phiên trò chuyện: {stats['total_sessions']}
• Trung bình mỗi ngày: {stats['avg_per_day']:.1f} cuộc

Phiên hiện tại: {self.sql_service.current_session_id or 'Chưa bắt đầu'}

Ngày bắt đầu sử dụng: {self.sql_service.get_first_use_date(self.user_name)}
"""
            else:
                info_text = f"Tên người dùng: {self.user_name}\n\nKhông có dữ liệu thống kê."
        except Exception as e:
            info_text = f"Tên người dùng: {self.user_name}\n\nKhông thể tải thống kê\nLỗi: {str(e)}"
        
        # Display info
        from PyQt6.QtWidgets import QTextEdit
        info_display = QTextEdit()
        info_display.setPlainText(info_text)
        info_display.setReadOnly(True)
        layout.addWidget(info_display)
        
        # Close button
        close_btn = QPushButton("Đóng")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)


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
        
        # Title
        title = QLabel(" Lịch sử sử dụng gần đây")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # History text
        self.history_text = QTextEdit()
        self.history_text.setReadOnly(True)
        
        # Load usage history (demo data)
        history_data = [
            f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Đăng nhập thành công",
            f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Mở cài đặt hệ thống",
            f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Sử dụng tính năng chat",
            f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Truy cập admin panel"
        ]
        
        self.history_text.setText("\n".join(history_data))
        layout.addWidget(self.history_text)
        
        # Buttons
        button_layout = QHBoxLayout()
        clear_btn = QPushButton("Xóa lịch sử")
        close_btn = QPushButton(" Đóng")
        button_layout.addWidget(clear_btn)
        button_layout.addWidget(close_btn)
        layout.addLayout(button_layout)
        
        # Handle buttons
        clear_btn.clicked.connect(self.clear_history)
        close_btn.clicked.connect(self.reject)
    
    def clear_history(self):
        """Clear history text"""
        self.history_text.clear()
        QMessageBox.information(self, "Thành công", "Đã xóa lịch sử sử dụng!")
