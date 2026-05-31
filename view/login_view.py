#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Login View - Pop Assistant
Giao diện đăng nhập đơn giản đẹp như giao diện chính
"""

import hashlib
import os
import random
import string
import sys

from PyQt6.QtCore import QDateTime, QPropertyAnimation, QRect, Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMenu,
    QMenuBar,
    QMessageBox,
    QPushButton,
    QSlider,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from view.ui_helpers import create_ui_footer, position_ui_footer


class LoginView(QDialog):
    login_success = pyqtSignal(str)
    
    def __init__(self, login_service):
        super().__init__()
        # Service injection - View nhận Service từ Controller, không tự tạo
        if login_service is None:
            raise ValueError("login_service is required - View must receive Service from Controller")
        self.login_service = login_service

        self.settings = self.login_service.load_settings()
        self.init_ui()
    
    def init_ui(self):
        """Khởi tạo giao diện đăng nhập đơn giản"""
        self.setWindowTitle("Pop Assistant")
        self.setFixedSize(400, 550)
        
        # Set style giống giao diện chính
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                               stop:0 #0f0f1a, stop:1 #1a1a2a);
            }
            QLineEdit {
                background: rgba(25, 25, 45, 180);
                border: 1px solid rgba(0, 255, 136, 40);
                border-radius: 10px;
                padding: 12px;
                color: rgba(255, 255, 255, 240);
                font-size: 15px;
                font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
                min-width: 200px;
                min-height: 20px;
            }
            QLineEdit:focus {
                border: 2px solid rgba(0, 255, 136, 80);
                background: rgba(25, 25, 45, 220);
            }
            QPushButton {
                background: rgba(0, 255, 136, 20);
                border: 1px solid rgba(0, 255, 136, 50);
                border-radius: 10px;
                padding: 12px 25px;
                color: rgba(0, 255, 136, 240);
                font-size: 15px;
                font-weight: 600;
                font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
                min-width: 200px;
                min-height: 20px;
            }
            QPushButton:hover {
                background: rgba(0, 255, 136, 40);
                border: 1px solid rgba(0, 255, 136, 80);
                color: rgba(0, 255, 136, 255);
            }
            QPushButton:pressed {
                background: rgba(0, 255, 136, 60);
                color: rgba(0, 255, 136, 255);
            }
            QLabel {
                color: rgba(255, 255, 255, 220);
                font-size: 15px;
                font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
                padding: 5px;
            }
        """)
        
        # Main layout
        layout = QVBoxLayout()
        layout.setSpacing(35)
        layout.setContentsMargins(50, 80, 50, 80)
        self.setLayout(layout)
        
        # Title
        title = QLabel("Pop Assistant")
        title.setStyleSheet("""
            QLabel {
                color: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                               stop:0 #00ffaa, stop:1 #00ccff);
                font-size: 32px;
                font-weight: 300;
                font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
                text-align: center;
                padding: 20px;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Username
        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText("Tên đăng nhập")
        layout.addWidget(self.login_username)
        
        # Password
        self.login_password = QLineEdit()
        self.login_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_password.setPlaceholderText("Mật khẩu")
        layout.addWidget(self.login_password)
        
        # Login button
        login_btn = QPushButton("Đăng nhập")
        login_btn.clicked.connect(self.login)
        layout.addWidget(login_btn)
        
        # Register text
        register_layout = QHBoxLayout()
        register_layout.addStretch()
        
        register_label = QLabel("Chưa có tài khoản? Đăng ký")
        register_label.setStyleSheet("""
            QLabel {
                color: rgba(0, 255, 136, 200);
                font-size: 13px;
                font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
                padding: 10px;
                font-weight: 500;
            }
        """)
        register_label.setCursor(Qt.CursorShape.PointingHandCursor)
        register_label.mousePressEvent = self.show_register_dialog
        register_layout.addWidget(register_label)
        register_layout.addStretch()
        
        layout.addLayout(register_layout)
        create_ui_footer(self)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        position_ui_footer(self)

    def save_settings(self):
        """Lưu cài đặt người dùng qua Service"""
        self.login_service.save_settings(self.settings)
    
    def show_settings_dialog(self):
        """Hiển thị dialog cài đặt hệ thống"""
        dialog = QDialog(self)
        dialog.setWindowTitle("🔧 Tùy chỉnh hệ thống")
        dialog.setFixedSize(450, 400)
        dialog.setStyleSheet("""
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
        
        layout = QVBoxLayout(dialog)
        
        # Auto start assistant
        auto_start_cb = QCheckBox("🚀 Tự động khởi động assistant")
        auto_start_cb.setChecked(self.settings.get("auto_start_assistant", True))
        
        # Assistant delay
        delay_layout = QHBoxLayout()
        delay_label = QLabel("⏱️ Thời gian trễ (ms):")
        delay_spin = QSpinBox()
        delay_spin.setRange(100, 5000)
        delay_spin.setValue(self.settings.get("assistant_delay", 1000))
        delay_layout.addWidget(delay_label)
        delay_layout.addWidget(delay_spin)
        delay_layout.addStretch()
        
        # Speech recognition
        speech_cb = QCheckBox("🎤 Nhận dạng giọng nói")
        speech_cb.setChecked(self.settings.get("speech_recognition", True))
        
        # Text to speech
        tts_cb = QCheckBox("🔊 Đọc văn bản thành giọng nói")
        tts_cb.setChecked(self.settings.get("text_to_speech", True))
        
        # Volume
        volume_layout = QHBoxLayout()
        volume_label = QLabel("🔊 Âm lượng:")
        volume_slider = QSlider(Qt.Orientation.Horizontal)
        volume_slider.setRange(0, 100)
        volume_slider.setValue(self.settings.get("volume", 80))
        volume_layout.addWidget(volume_label)
        volume_layout.addWidget(volume_slider)
        volume_layout.addStretch()
        
        # Speech rate
        rate_layout = QHBoxLayout()
        rate_label = QLabel("⚡ Tốc độ nói:")
        rate_spin = QSpinBox()
        rate_spin.setRange(50, 200)
        rate_spin.setValue(int(self.settings.get("speech_rate", 1.0) * 100))
        rate_layout.addWidget(rate_label)
        rate_layout.addWidget(rate_spin)
        rate_layout.addStretch()
        
        # Add widgets to layout
        layout.addWidget(auto_start_cb)
        layout.addLayout(delay_layout)
        layout.addWidget(speech_cb)
        layout.addWidget(tts_cb)
        layout.addLayout(volume_layout)
        layout.addLayout(rate_layout)
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("💾 Lưu")
        cancel_btn = QPushButton("❌ Hủy")
        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        # Handle buttons
        def save_settings():
            self.settings["auto_start_assistant"] = auto_start_cb.isChecked()
            self.settings["assistant_delay"] = delay_spin.value()
            self.settings["speech_recognition"] = speech_cb.isChecked()
            self.settings["text_to_speech"] = tts_cb.isChecked()
            self.settings["volume"] = volume_slider.value()
            self.settings["speech_rate"] = rate_spin.value() / 100.0
            
            self.save_settings()
            QMessageBox.information(dialog, "Thành công", "Đã lưu cài đặt!")
            dialog.accept()
        
        save_btn.clicked.connect(save_settings)
        cancel_btn.clicked.connect(dialog.reject)
        
        dialog.exec()
    
    def show_audio_dialog(self):
        """Hiển thị dialog cài đặt âm thanh"""
        dialog = QDialog(self)
        dialog.setWindowTitle("🔊 Cài đặt âm thanh")
        dialog.setFixedSize(400, 300)
        dialog.setStyleSheet("""
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
        
        layout = QVBoxLayout(dialog)
        
        # Volume
        volume_layout = QHBoxLayout()
        volume_label = QLabel("🔊 Âm lượng chính:")
        volume_slider = QSlider(Qt.Orientation.Horizontal)
        volume_slider.setRange(0, 100)
        volume_slider.setValue(self.settings.get("volume", 80))
        volume_layout.addWidget(volume_label)
        volume_layout.addWidget(volume_slider)
        volume_layout.addStretch()
        
        # Speech rate
        rate_layout = QHBoxLayout()
        rate_label = QLabel("⚡ Tốc độ nói:")
        rate_spin = QSpinBox()
        rate_spin.setRange(50, 200)
        rate_spin.setValue(int(self.settings.get("speech_rate", 1.0) * 100))
        rate_layout.addWidget(rate_label)
        rate_layout.addWidget(rate_spin)
        rate_layout.addStretch()
        
        # Add widgets
        layout.addLayout(volume_layout)
        layout.addLayout(rate_layout)
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("💾 Lưu")
        cancel_btn = QPushButton("❌ Hủy")
        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        # Handle buttons
        def save_audio():
            self.settings["volume"] = volume_slider.value()
            self.settings["speech_rate"] = rate_spin.value() / 100.0
            
            self.save_settings()
            QMessageBox.information(dialog, "Thành công", "Đã lưu cài đặt âm thanh!")
            dialog.accept()
        
        save_btn.clicked.connect(save_audio)
        cancel_btn.clicked.connect(dialog.reject)
        
        dialog.exec()
    
    
    
    def show_toast(self, message, is_success=True):
        """Hiển thị toast đơn giản trên dialog"""
        # Tạo label trực tiếp trên dialog
        toast_label = QLabel(message, self)
        toast_label.setFixedSize(300, 50)
        toast_label.setStyleSheet(f"""
            QLabel {{
                background: {'rgba(81, 207, 102, 200)' if is_success else 'rgba(255, 107, 107, 200)'};
                border: 1px solid {'rgba(81, 207, 102, 100)' if is_success else 'rgba(255, 107, 107, 100)'};
                border-radius: 8px;
                color: white;
                font-size: 14px;
                font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
                font-weight: 500;
                padding: 10px;
            }}
        """)
        toast_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Đặt vị trí ở trên cùng của dialog
        x = (self.width() - toast_label.width()) // 2
        y = 20  # Cách top 20px
        
        toast_label.move(x, y)
        toast_label.show()
        toast_label.raise_()
        
        print(f"Toast hien thi: {message} tai ({x}, {y})")
        
        # Tự động ẩn sau 3 giây
        QTimer.singleShot(3000, toast_label.deleteLater)
    
    def show_register_dialog(self, event):
        """Hiển thị dialog đăng ký"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Đăng ký")
        dialog.setFixedSize(400, 400)  # Tăng kích thước cho 3 ô
        dialog.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                               stop:0 #0f0f1a, stop:1 #1a1a2a);
            }
            QLineEdit {
                background: rgba(25, 25, 45, 180);
                border: 1px solid rgba(0, 255, 136, 40);
                border-radius: 8px;
                padding: 12px;
                color: white;
                font-size: 14px;
                font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
                min-width: 250px;
            }
            QPushButton {
                background: rgba(0, 255, 136, 20);
                border: 1px solid rgba(0, 255, 136, 50);
                border-radius: 8px;
                padding: 12px 20px;
                color: rgba(0, 255, 136, 240);
                font-size: 14px;
                font-weight: 600;
                font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
                min-width: 100px;
            }
            QPushButton:hover {
                background: rgba(0, 255, 136, 40);
                color: rgba(0, 255, 136, 255);
            }
            QPushButton#cancel {
                background: rgba(255, 107, 107, 20);
                border: 1px solid rgba(255, 107, 107, 50);
                color: rgba(255, 107, 107, 240);
            }
            QPushButton#cancel:hover {
                background: rgba(255, 107, 107, 40);
                color: rgba(255, 107, 107, 255);
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)  # Tăng spacing
        layout.setContentsMargins(30, 30, 30, 30)  # Tăng margins
        
        # Title
        title = QLabel("Đăng ký tài khoản")
        title.setStyleSheet("""
            QLabel {
                color: rgba(0, 255, 136, 240);
                font-size: 16px;
                font-weight: 600;
                font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
                padding: 15px;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Username
        username = QLineEdit()
        username.setPlaceholderText("Tên đăng ký")
        layout.addWidget(username)
        
        # Password
        password = QLineEdit()
        password.setEchoMode(QLineEdit.EchoMode.Password)
        password.setPlaceholderText("Mật khẩu đăng ký")
        layout.addWidget(password)
        
        # Captcha
        captcha_container = QWidget()
        captcha_container.setFixedHeight(50)
        captcha_layout = QHBoxLayout(captcha_container)
        captcha_layout.setSpacing(15)
        captcha_layout.setContentsMargins(0, 0, 0, 0)
        
        captcha_input = QLineEdit()
        captcha_input.setPlaceholderText("Mã captcha")
        captcha_input.setMaxLength(4)
        captcha_input.setFixedWidth(20)
        
        # Tạo captcha ngẫu nhiên
        captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        
        # Chuyển captcha thành button
        captcha_button = QPushButton(captcha_text)
        captcha_button.setStyleSheet("""
            QPushButton {
                background: rgba(0, 255, 136, 20);
                border: 1px solid rgba(0, 255, 136, 50);
                border-radius: 8px;
                color: rgba(0, 255, 136, 240);
                font-size: 16px;
                font-weight: bold;
                font-family: 'Courier New', monospace;
                padding: 10px 6px;
                min-width: 45px;
                max-width: 45px;
            }
            QPushButton:hover {
                background: rgba(0, 255, 136, 40);
                border: 1px solid rgba(0, 255, 136, 80);
            }
            QPushButton:pressed {
                background: rgba(0, 255, 136, 60);
            }
        """)
        
        def refresh_captcha():
            new_captcha = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            captcha_button.setText(new_captcha)
            captcha_input.clear()
            captcha_input.setFocus()
        
        captcha_button.clicked.connect(refresh_captcha)
        
        # Thêm vào layout
        captcha_layout.addWidget(captcha_input)
        captcha_layout.addWidget(captcha_button)
        
        # Thêm container vào main layout
        layout.addWidget(captcha_container)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)  # Spacing giữa buttons
        
        register_btn = QPushButton("Đăng ký")
        cancel_btn = QPushButton("Hủy")
        cancel_btn.setObjectName("cancel")
        
        btn_layout.addWidget(register_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
        dialog.setLayout(layout)
        
        def do_register():
            uname = username.text().strip()
            pwd = password.text()
            captcha_entered = captcha_input.text().strip()
            
            if not uname or not pwd or not captcha_entered:
                QMessageBox.warning(dialog, "Thông báo", "Vui lòng nhập đầy đủ thông tin!")
                return
            
            if len(uname) < 3:
                QMessageBox.warning(dialog, "Lỗi", "Tên phải có ít nhất 3 ký tự!")
                return
            
            if len(pwd) < 6:
                QMessageBox.warning(dialog, "Lỗi", "Mật khẩu phải có ít nhất 6 ký tự!")
                return
            
            if captcha_entered != captcha_button.text():
                QMessageBox.warning(dialog, "Lỗi", "Mã captcha không đúng!")
                refresh_captcha()  # Tạo captcha mới
                return
            
            # Check if user exists
            if self.login_service.user_exists(uname):
                QMessageBox.warning(dialog, "Lỗi", "Tên đã tồn tại!")
                return
            
            # Register via Service
            if self.login_service.save_new_user(uname, pwd):
                QMessageBox.information(dialog, "Thành công", "Đăng ký thành công!")
                dialog.accept()
            else:
                QMessageBox.warning(dialog, "Lỗi", "Đăng ký thất bại!")
        
        register_btn.clicked.connect(do_register)
        cancel_btn.clicked.connect(dialog.reject)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.login_username.setText(username.text())
            self.login_password.clear()
    
    def login(self):
        """Xử lý đăng nhập - View chỉ gọi Service, không xử lý logic"""
        username = self.login_username.text().strip()
        password = self.login_password.text()
        
        if not username or not password:
            self.show_toast("Vui lòng nhập đầy đủ thông tin!", False)
            return
        
        # Xác thực qua Service - View không biết chi tiết
        if self.login_service.authenticate_user(username, password):
            self.show_toast("Đăng nhập thành công!", True)
            try:
                self.login_success.emit(username)
            except Exception as e:
                import traceback
                traceback.print_exc()
        else:
            if self.login_service.user_exists(username):
                self.show_toast("Mật khẩu không đúng!", False)
            else:
                self.show_toast("Tên đăng nhập không tồn tại!", False)
    

def main():
    app = QApplication(sys.argv)
    login_window = LoginView()
    login_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
