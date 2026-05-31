#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Conversation History Viewer
Xem lịch sử cuộc trò chuyện
"""
import os
import sys

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QSplitter,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from database.conversation_db import ConversationDB


class HistoryViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = ConversationDB()
        self.current_user = "bạn"
        self.init_ui()
        self.load_user_list()
    
    def init_ui(self):
        """Khởi tạo giao diện"""
        self.setWindowTitle("Lịch sử trò chuyện - Pop Assistant")
        self.setGeometry(150, 150, 800, 600)
        
        # Set modern dark theme
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                               stop:0 #0f0f1a, stop:1 #1a1a2a);
            }
            QListWidget {
                background: rgba(20, 20, 35, 200);
                border: 1px solid rgba(0, 255, 136, 30);
                border-radius: 10px;
                padding: 10px;
                color: white;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 8px;
                margin: 2px;
                border-radius: 5px;
            }
            QListWidget::item:selected {
                background: rgba(0, 255, 136, 30);
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
                padding: 10px 20px;
                color: #00ff88;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(0, 255, 136, 40);
            }
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 5px;
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("Lịch sử trò chuyện")
        title.setStyleSheet("""
            QLabel {
                color: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                               stop:0 #00ffaa, stop:1 #00ccff);
                font-size: 24px;
                font-weight: 300;
                text-align: center;
                padding: 15px;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton("Làm mới")
        self.refresh_btn.clicked.connect(self.refresh_data)
        button_layout.addWidget(self.refresh_btn)
        
        self.clear_btn = QPushButton("Xóa cũ (>30 ngày)")
        self.clear_btn.clicked.connect(self.clear_old_data)
        button_layout.addWidget(self.clear_btn)
        
        button_layout.addStretch()
        main_layout.addLayout(button_layout)
        
        # Splitter for list and content
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left side - Sessions list
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        sessions_label = QLabel("Các phiên trò chuyện:")
        left_layout.addWidget(sessions_label)
        
        self.sessions_list = QListWidget()
        self.sessions_list.itemClicked.connect(self.load_session_conversations)
        left_layout.addWidget(self.sessions_list)
        
        splitter.addWidget(left_widget)
        
        # Right side - Conversation content
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        content_label = QLabel("Nội dung trò chuyện:")
        right_layout.addWidget(content_label)
        
        self.conversation_text = QTextEdit()
        self.conversation_text.setReadOnly(True)
        right_layout.addWidget(self.conversation_text)
        
        splitter.addWidget(right_widget)
        
        # Set splitter sizes
        splitter.setSizes([300, 500])
        main_layout.addWidget(splitter)
    
    def load_user_list(self):
        """Tải danh sách phiên trò chuyện"""
        try:
            # Lấy tất cả các phiên của người dùng hiện tại
            sessions = self.db.get_all_sessions(self.current_user)
            
            self.sessions_list.clear()
            
            for session in sessions:
                session_id, start_time, end_time = session
                # Format thời gian
                start_str = start_time.replace('T', ' ')[:19] if start_time else "Unknown"
                end_str = end_time.replace('T', ' ')[:19] if end_time else "Đang hoạt động"
                
                item_text = f"{start_str} - {end_str}"
                item = QListWidgetItem(item_text)
                item.setData(Qt.ItemDataRole.UserRole, session_id)
                self.sessions_list.addItem(item)
                
        except Exception as e:
            print(f"Error loading sessions: {e}")
    
    def load_session_conversations(self, item):
        """Tải nội dung cuộc trò chuyện của phiên được chọn"""
        try:
            session_id = item.data(Qt.ItemDataRole.UserRole)
            conversations = self.db.get_session_conversations(session_id, self.current_user)
            
            content = f"Phiên trò chuyện: {session_id}\n"
            content += "=" * 50 + "\n\n"
            
            for conv in conversations:
                user_msg, bot_response, timestamp = conv
                time_str = timestamp.replace('T', ' ')[:19] if timestamp else "Unknown"
                
                content += f" {time_str}\n"
                content += f" Bạn: {user_msg}\n"
                content += f" Pop: {bot_response}\n"
                content += "-" * 30 + "\n\n"
            
            self.conversation_text.setPlainText(content)
            
        except Exception as e:
            print(f"Error loading conversations: {e}")
            self.conversation_text.setPlainText("Lỗi khi tải cuộc trò chuyện")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        position_ui_footer(self)
        print("Data refreshed")
    
    def clear_old_data(self):
        """Xóa dữ liệu cũ"""
        try:
            self.db.delete_old_conversations(30)
            self.refresh_data()
            print("Old conversations deleted")
        except Exception as e:
            print(f"Error deleting old data: {e}")

def main():
    app = QApplication(sys.argv)
    viewer = HistoryViewer()
    viewer.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
