#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pop Assistant - Admin Login Panel
Giao diện đăng nhập admin với Konami Code
"""

import hashlib
import os
import sys

from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QPalette
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from database.admin_repository import AdminRepository
from utils.logger import get_logger
from view.ui_helpers import create_ui_footer, position_ui_footer

logger = get_logger(__name__)

# Rely on package imports; avoid sys.path hacks

class AdminLoginView(QDialog):
    """Admin Login Interface"""
    login_success = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(" Admin Assistant")
        self.setFixedSize(400, 550)  # Giống login thường
        
        # Key tracking
        self.pressed_keys = []
        self.ctrl_count = 0  # Đếm số lần Ctrl
        
        # Setup UI
        self.setup_ui()
        self.setup_style()
        
        # Setup key press timer
        self.key_timer = QTimer()
        self.key_timer.timeout.connect(self.clear_keys)
        self.key_timer.setSingleShot(True)
        
    def setup_ui(self):
        """Create admin login interface exactly like login view"""
        # Main layout - giống hệt login thường
        layout = QVBoxLayout(self)
        layout.setSpacing(35)  # Giống login thường
        layout.setContentsMargins(50, 80, 50, 80)  # Giống login thường
        
        # Title - giống hệt login thường
        title = QLabel("Admin Assistant")
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
        
        # Password field - giống hệt login thường
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Mật khẩu admin")
        self.password_input.setStyleSheet("""
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
                color: rgba(255, 255, 255, 240);
            }
        """)
        layout.addWidget(self.password_input)
        
        # Login button - giống hệt login thường
        login_btn = QPushButton("Đăng nhập")
        login_btn.setStyleSheet("""
            QPushButton {
                background: rgba(0, 255, 136, 20);
                border: 1px solid rgba(0, 255, 136, 50);
                border-radius: 10px;
                padding: 12px 25px;
                color: rgba(0, 255, 136, 240);
                font-size: 15px;
                font-weight: 600;
                font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
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
        """)
        login_btn.clicked.connect(self.admin_login)
        layout.addWidget(login_btn)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                color: #ff6b6b;
                font-size: 14px;
                margin-top: 10px;
                font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
            }
        """)
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
        self.setLayout(layout)
        create_ui_footer(self)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        position_ui_footer(self)
    
    def admin_login(self):
        """Handle admin login"""
        try:
            password = self.password_input.text().strip()
            
            if not password:
                self.status_label.setText("Vui lòng nhập mật khẩu admin!")
                return
            
            # Load admin password from config
            stored_hash = self.get_admin_password_hash()
            
            # Hash input password
            input_hash = hashlib.sha256(password.encode()).hexdigest()
            
            # Debug
            print(f"Input password: {password}")
            print(f"Input hash: {input_hash}")
            print(f"Stored hash: {stored_hash}")
            
            # Verify password
            if input_hash == stored_hash:
                self.status_label.setText("Đăng nhập admin thành công!")
                self.login_success.emit("admin")
                QTimer.singleShot(1000, self.close)
            else:
                self.status_label.setText("Sai mật khẩu admin!")
                
        except Exception as e:
            print(f"Lỗi đăng nhập admin: {e}")
            self.status_label.setText("Lỗi đăng nhập!")
    
    def get_admin_password_hash(self):
        """Get admin password hash from repository."""
        try:
            repo = AdminRepository()
            pw = repo.get_admin_password_hash('admin')
            if pw:
                return pw
            return hashlib.sha256("admin123".encode()).hexdigest()
        except Exception as e:
            logger.error("Error reading admin password: %s", e, exc_info=True)
            return hashlib.sha256("admin123".encode()).hexdigest()
    
    def clear_keys(self):
        """Clear pressed keys"""
        self.pressed_keys = []
        self.ctrl_count = 0
        self.status_label.setText("")

    def setup_style(self):
        """Apply style exactly like login view"""
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
    
    def keyPressEvent(self, event):
        """Handle key press events for Ctrl detection"""
        key = event.key()
        
        # Detect Ctrl key
        if key == Qt.Key.Key_Control:
            self.ctrl_count += 1
            if self.ctrl_count >= 3:
                self.open_change_password_dialog()
                self.ctrl_count = 0
            else:
                # Start timer to clear count after 2 seconds
                self.key_timer.start(2000)
        else:
            # Clear count if other key pressed
            self.ctrl_count = 0
        
        super().keyPressEvent(event)
    
    def open_change_password_dialog(self):
        """Open dialog to change admin password (không cần mật khẩu hiện tại)"""
        from PyQt6.QtWidgets import QInputDialog, QMessageBox

        # Hiển thị thông báo
        reply = QMessageBox.question(
            self, "Đổi Mật Khẩu Admin", 
            "Bạn muốn đổi mật khẩu admin?\n\nĐây là tính năng khôi phục mật khẩu khi quên.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            new_password, ok = QInputDialog.getText(
                self, "Đổi Mật Khẩu Admin", "Nhập mật khẩu admin mới:", 
                QLineEdit.EchoMode.Password
            )
            
            if ok and new_password:
                confirm_password, ok = QInputDialog.getText(
                    self, "Đổi Mật Khẩu Admin", "Xác nhận mật khẩu mới:", 
                    QLineEdit.EchoMode.Password
                )
                
                if ok and confirm_password:
                    if new_password == confirm_password:
                        if len(new_password) >= 4:
                            self.save_new_password(new_password)
                            self.status_label.setText(" Đổi mật khẩu thành công!")
                        else:
                            self.status_label.setText(" Mật khẩu phải có ít nhất 4 ký tự!")
                    else:
                        self.status_label.setText("Mật khẩu xác nhận không khớp!")

    def save_new_password(self, new_password):
        import hashlib
        try:
            new_hash = hashlib.sha256(new_password.encode()).hexdigest()
            repo = AdminRepository()
            ok = repo.update_admin_password('admin', new_hash)
            if ok:
                logger.info("Admin password updated")
                self.status_label.setText("Đổi mật khẩu thành công")
            else:
                self.status_label.setText("Lỗi lưu mật khẩu!")
        except Exception as e:
            logger.error("Error saving new password: %s", e, exc_info=True)
            self.status_label.setText("Lỗi lưu mật khẩu!")

def main():
    """Main function to run admin login"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Pop Assistant Admin")
    app.setOrganizationName("Pop AI")
    
    # Create admin login window
    admin_login = AdminLoginView()
    admin_login.show()
    
    # Run application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
