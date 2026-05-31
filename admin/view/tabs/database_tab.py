#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pop Assistant - Database Tab
Tab quản lý database
"""

import json
import os
import shutil
from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
)

from admin.view.styles import (
    BUTTON_BLUE,
    BUTTON_GREEN,
    BUTTON_ORANGE,
    BUTTON_RED,
    DIALOG_CONVERSATION,
    DIALOG_MAIN,
    INFO_FRAME,
    INFO_LABEL,
    LOG_TEXT,
    TABLE_WIDGET,
)
from admin.view.tabs.base_tab import BaseTab
from database.admin_repository import AdminRepository
from utils.logger import get_logger

logger = get_logger(__name__)


class DatabaseTab(BaseTab):
    """Tab quản lý database"""
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Database info
        info_frame = QFrame()
        info_frame.setStyleSheet(INFO_FRAME)
        info_layout = QVBoxLayout(info_frame)
        
        self.db_info_label = QLabel("Đang tải thông tin database...")
        self.db_info_label.setStyleSheet(INFO_LABEL)
        info_layout.addWidget(self.db_info_label)
        layout.addWidget(info_frame)
        
        # Database operations
        ops_frame = QFrame()
        ops_layout = QGridLayout(ops_frame)
        
        # Backup button
        backup_btn = QPushButton("Backup Database")
        backup_btn.setStyleSheet(BUTTON_GREEN)
        backup_btn.clicked.connect(self.backup_database)
        ops_layout.addWidget(backup_btn, 0, 0)
        
        # Restore button
        restore_btn = QPushButton("Restore Database")
        restore_btn.setStyleSheet(BUTTON_ORANGE)
        restore_btn.clicked.connect(self.restore_database)
        ops_layout.addWidget(restore_btn, 0, 1)
        
        # Clear old data button
        clear_btn = QPushButton("Xóa dữ liệu cũ")
        clear_btn.setStyleSheet(BUTTON_RED)
        clear_btn.clicked.connect(self.clear_old_data)
        ops_layout.addWidget(clear_btn, 1, 0)
        
        # Export button
        export_btn = QPushButton("Export Data")
        export_btn.setStyleSheet(BUTTON_BLUE)
        export_btn.clicked.connect(self.export_data)
        ops_layout.addWidget(export_btn, 1, 1)
        
        layout.addWidget(ops_frame)
        
        # Log area
        log_frame = QFrame()
        log_layout = QVBoxLayout(log_frame)
        
        log_label = QLabel("Operation Log:")
        log_layout.addWidget(log_label)
        
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(200)
        self.log_text.setStyleSheet(LOG_TEXT)
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        
        layout.addWidget(log_frame)
        layout.addStretch()
    
    def log(self, message):
        """Override log to write to text widget"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
    
    def log_message(self, message):
        """Alias for log - for compatibility with admin_panel"""
        self.log(message)
    
    def load_data(self):
        """Load database information"""
        try:
            if not os.path.exists(self.db_path):
                self.db_info_label.setText("Database không tồn tại")
                return
                
            size = os.path.getsize(self.db_path)
            size_mb = size / (1024 * 1024)
            repo = AdminRepository(self.db_path)
            stats = repo.get_user_statistics()
            total_conversations = stats.get('total_conversations', 0)
            try:
                active_sessions = repo.get_active_sessions_count()
            except Exception:
                active_sessions = 0
            
            self.db_info_label.setText(
                f"Database Size: {size_mb:.2f} MB\n"
                f"Total Conversations: {total_conversations}\n"
                f"Active Sessions: {active_sessions}"
            )
            self.log("Database info loaded")
        except Exception as e:
            self.db_info_label.setText(f"Lỗi: {e}")
            self.log(f"Error: {e}")
    
    def backup_database(self):
        """Backup database"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"backup_conversations_{timestamp}.db"
            
            if os.path.exists(self.db_path):
                shutil.copy2(self.db_path, backup_file)
                self.log(f"Backup thành công: {backup_file}")
                QMessageBox.information(self, "Thành công", f"Database đã backup: {backup_file}")
            else:
                QMessageBox.warning(self, "Lỗi", "Không tìm thấy file database!")
        except Exception as e:
            self.log(f"Lỗi backup: {e}")
            QMessageBox.critical(self, "Lỗi", f"Lỗi backup: {e}")
    
    def restore_database(self):
        """Restore database"""
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Database Files (*.db)")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        
        if file_dialog.exec():
            files = file_dialog.selectedFiles()
            if files:
                try:
                    shutil.copy2(files[0], self.db_path)
                    self.log(f"Database restored từ: {files[0]}")
                    QMessageBox.information(self, "Thành công", "Database restored!")
                    self.load_data()
                except Exception as e:
                    self.log(f"Lỗi restore: {e}")
                    QMessageBox.critical(self, "Lỗi", f"Lỗi restore: {e}")
    
    def clear_old_data(self):
        """Clear old data"""
        reply = QMessageBox.question(
            self, "Xác nhận", "Xóa dữ liệu cũ (trước 30 ngày)?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                repo = AdminRepository(self.db_path)
                deleted = repo.cleanup_old_data(days=30)
                self.log(f"Đã xóa dữ liệu cũ: {deleted} records")
                QMessageBox.information(self, "Thành công", "Đã xóa dữ liệu cũ!")
                self.load_data()
            except Exception as e:
                self.log(f"Lỗi xóa dữ liệu: {e}")
                QMessageBox.critical(self, "Lỗi", f"Lỗi xóa dữ liệu: {e}")
    
    def export_data(self):
        """Export data to JSON"""
        try:
            repo = AdminRepository(self.db_path)
            users = repo.export_users()

            # sessions table may not have an export helper; fetch via repository connection
            conn = repo._get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT * FROM sessions")
                sessions = cursor.fetchall()
            except Exception:
                sessions = []
            conn.close()

            export_data = {
                "users": users,
                "sessions": sessions,
                "export_date": datetime.now().isoformat()
            }
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            export_file = f"export_data_{timestamp}.json"
            
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            self.log(f"Data exported: {export_file}")
            QMessageBox.information(self, "Thành công", f"Data exported: {export_file}")
            
        except Exception as e:
            self.log(f"Lỗi export: {e}")
            QMessageBox.critical(self, "Lỗi", f"Lỗi export: {e}")
