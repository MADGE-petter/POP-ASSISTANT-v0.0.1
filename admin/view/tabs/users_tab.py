#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pop Assistant - Users Tab
Tab quản lý người dùng
"""

import hashlib
import os
from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidgetItem,
    QVBoxLayout,
)

from admin.view.styles import (
    BUTTON_BLUE,
    BUTTON_GREEN,
    BUTTON_ORANGE,
    BUTTON_RED,
    DIALOG_MAIN,
    TABLE_WIDGET,
)
from admin.view.tabs.base_tab import BaseTab
from database.admin_repository import AdminRepository
from utils.logger import get_logger

logger = get_logger(__name__)


class UsersTab(BaseTab):
    """Tab quản lý người dùng"""
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Online users counter
        self.online_label = QLabel("🟢 Online: 0 | ⚫ Offline: 0")
        layout.addWidget(self.online_label)
        
        # Users table - thêm cột Status với màu
        self.users_table = self.create_table(
            5, ["Username", "Password Hash", "Created Date", "Status", "Last Active"], TABLE_WIDGET
        )
        layout.addWidget(self.users_table)
        
        # Control buttons
        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        
        # Add user button
        add_user_btn = QPushButton("Thêm User")
        add_user_btn.setStyleSheet(BUTTON_GREEN)
        add_user_btn.clicked.connect(self.add_user)
        button_layout.addWidget(add_user_btn)
        
        # Delete user button
        delete_user_btn = QPushButton("Xóa User")
        delete_user_btn.setStyleSheet(BUTTON_RED)
        delete_user_btn.clicked.connect(self.delete_user)
        button_layout.addWidget(delete_user_btn)
        
        # Reset password button
        reset_pwd_btn = QPushButton("Reset Password")
        reset_pwd_btn.setStyleSheet(BUTTON_ORANGE)
        reset_pwd_btn.clicked.connect(self.reset_password)
        button_layout.addWidget(reset_pwd_btn)
        
        button_layout.addStretch()
        
        # Refresh button
        refresh_btn = QPushButton("Làm mới")
        refresh_btn.setStyleSheet(BUTTON_BLUE)
        refresh_btn.clicked.connect(self.load_data)
        button_layout.addWidget(refresh_btn)
        
        layout.addWidget(button_frame)
    
    def load_data(self):
        """Load users from database với trạng thái online/offline"""
        try:
            if not os.path.exists(self.db_path):
                self.log(f"Database not found: {self.db_path}")
                return
            repo = AdminRepository(self.db_path)
            conn = repo._get_connection()
            cursor = conn.cursor()

            # Check if users table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
            if not cursor.fetchone():
                self._show_empty_message("Bảng 'users' không tồn tại")
                conn.close()
                self.log("Table 'users' not found")
                return

            # Lấy danh sách active sessions (online users)
            active_sessions = self._get_active_sessions(cursor)
            online_count = len(active_sessions)

            cursor.execute("SELECT tenNguoiDung, matKhauMaHoa, thoiGianTao, maNguoiDung FROM users ORDER BY thoiGianTao DESC")
            users = cursor.fetchall() or []

            logger.debug("DEBUG: Fetched %d rows from DB, %d online", len(users), online_count)

            self.users_table.setRowCount(0)
            offline_count = 0
            if not users:
                self._show_empty_message("Chưa có user nào")
            else:
                displayed_count = 0
                for username, password_hash, created_date, user_id in users:
                    logger.debug("DEBUG: User=%s", username)
                    if not password_hash:  # Skip display names
                        logger.debug("DEBUG: Skipping %s - no password", username)
                        continue

                    # Check if user is online
                    is_online = user_id in active_sessions
                    session_info = active_sessions.get(user_id, {})

                    row = self.users_table.rowCount()
                    self.users_table.insertRow(row)
                    self.users_table.setItem(row, 0, QTableWidgetItem(username))
                    masked = (password_hash[:8] + "...") if len(password_hash) > 8 else password_hash
                    self.users_table.setItem(row, 1, QTableWidgetItem(masked))
                    self.users_table.setItem(row, 2, QTableWidgetItem(created_date))

                    # Status with color
                    status_item = QTableWidgetItem("🟢 Online" if is_online else "⚫ Offline")
                    if is_online:
                        status_item.setBackground(Qt.GlobalColor.darkGreen)
                        status_item.setForeground(Qt.GlobalColor.white)
                    else:
                        offline_count += 1
                    self.users_table.setItem(row, 3, status_item)

                    # Last active time
                    last_active = session_info.get('start_time', 'Never')
                    self.users_table.setItem(row, 4, QTableWidgetItem(str(last_active)))

                    displayed_count += 1
                logger.debug("DEBUG: Displayed %d users (%d online)", displayed_count, online_count)

            conn.close()

            # Update counter label
            self.online_label.setText(f"🟢 Online: {online_count} | ⚫ Offline: {offline_count}")

            self.log(f"Loaded {len(users)} users ({online_count} online)")
        except Exception as e:
            self.log(f"Error: {e}")
    
    def _get_active_sessions(self, cursor) -> dict:
        """Lấy danh sách active sessions (online users)"""
        try:
            cursor.execute("""
                SELECT maNguoiDung, thoiGianBatDau 
                FROM sessions 
                WHERE thoiGianKetThuc IS NULL
            """)
            sessions = {}
            for row in cursor.fetchall():
                user_id, start_time = row
                sessions[user_id] = {'start_time': start_time}
            return sessions
        except Exception as e:
            self.log(f"Error getting active sessions: {e}")
            return {}
    
    def add_user(self):
        """Add new user"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Thêm User Mới")
        dialog.setFixedSize(400, 300)
        dialog.setStyleSheet(DIALOG_MAIN)
        
        layout = QVBoxLayout(dialog)
        
        username_input = QLineEdit()
        username_input.setPlaceholderText("Nhập username...")
        
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_input.setPlaceholderText("Nhập password...")
        
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Lưu")
        cancel_btn = QPushButton("Hủy")
        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(username_input)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(password_input)
        layout.addStretch()
        layout.addLayout(button_layout)
        
        def save():
            username = username_input.text().strip()
            password = password_input.text().strip()
            
            if not username or not password:
                QMessageBox.warning(dialog, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
                return
            
            try:
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                repo = AdminRepository(self.db_path)
                conn = repo._get_connection()
                cursor = conn.cursor()

                cursor.execute("SELECT tenNguoiDung FROM users WHERE tenNguoiDung = ?", (username,))
                if cursor.fetchone():
                    QMessageBox.warning(dialog, "Lỗi", f"User '{username}' đã tồn tại!")
                    conn.close()
                    return

                created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute(
                    "INSERT INTO users (tenNguoiDung, matKhauMaHoa, thoiGianTao) VALUES (?, ?, ?)",
                    (username, password_hash, created_date)
                )
                conn.commit()
                conn.close()

                self.load_data()
                QMessageBox.information(dialog, "Thành công", f"Đã thêm user '{username}'!")
                dialog.accept()

            except Exception as e:
                QMessageBox.critical(dialog, "Lỗi", f"Lỗi thêm user: {e}")
        
        save_btn.clicked.connect(save)
        cancel_btn.clicked.connect(dialog.reject)
        dialog.exec()
    
    def delete_user(self):
        """Delete selected user"""
        current_row = self.users_table.currentRow()
        if current_row >= 0:
            username = self.users_table.item(current_row, 0).text()
            reply = QMessageBox.question(
                self, "Xác nhận", f"Xóa user '{username}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    repo = AdminRepository(self.db_path)
                    conn = repo._get_connection()
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM users WHERE tenNguoiDung = ?", (username,))
                    conn.commit()
                    conn.close()
                    self.log(f"Deleted user: {username}")
                    self.load_data()
                except Exception as e:
                    QMessageBox.critical(self, "Lỗi", f"Lỗi xóa user: {e}")
        else:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn user để xóa!")
    
    def reset_password(self):
        """Reset user password"""
        current_row = self.users_table.currentRow()
        if current_row >= 0:
            username = self.users_table.item(current_row, 0).text()
            QMessageBox.information(self, "Thông báo", f"Reset password cho '{username}' - tính năng đang phát triển")
        else:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn user!")
    
    def _show_empty_message(self, message):
        """Hiển thị thông báo khi không có dữ liệu"""
        self.users_table.setRowCount(1)
        self.users_table.setItem(0, 0, QTableWidgetItem(message))
        self.users_table.setSpan(0, 0, 1, 5)
        item = self.users_table.item(0, 0)
        if item:
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
