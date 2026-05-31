import sqlite3

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class HistoryWindow(QMainWindow):
    def __init__(self, db, user_name):
        super().__init__()
        self.db = db
        self.user_name = user_name
        self.init_ui()
        self.load_statistics()
    
    def init_ui(self):
        """Khởi tạo giao diện lịch sử"""
        self.setWindowTitle("Lịch sử trò chuyện - Pop Assistant")
        self.setGeometry(200, 200, 900, 700)
        
        # Set modern dark theme
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                               stop:0 #0f0f1a, stop:1 #1a1a2a);
            }
            QTabWidget::pane {
                border: 1px solid rgba(0, 255, 136, 30);
                background: rgba(20, 20, 35, 100);
                border-radius: 10px;
            }
            QTabBar::tab {
                background: rgba(0, 255, 136, 20);
                color: #00ff88;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: rgba(0, 255, 136, 40);
                border: 1px solid rgba(0, 255, 136, 60);
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
            QLabel {
                color: white;
                font-size: 14px;
                padding: 5px;
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
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel(f"Lịch sử trò chuyện của {self.user_name}")
        title.setStyleSheet("""
            QLabel {
                color: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                               stop:0 #00ffaa, stop:1 #00ccff);
                font-size: 20px;
                font-weight: 300;
                text-align: center;
                padding: 15px;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        
        # Tab 1: Thống kê
        self.stats_tab = QWidget()
        self.setup_stats_tab()
        self.tab_widget.addTab(self.stats_tab, "Thống kê")
        
        # Tab 2: Lịch sử chi tiết
        self.history_tab = QWidget()
        self.setup_history_tab()
        self.tab_widget.addTab(self.history_tab, " Chi tiết")
        
        main_layout.addWidget(self.tab_widget)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        refresh_btn = QPushButton(" Làm mới")
        refresh_btn.clicked.connect(self.refresh_data)
        button_layout.addWidget(refresh_btn)
        
        clear_btn = QPushButton(" Xóa cũ (>30 ngày)")
        clear_btn.clicked.connect(self.clear_old_data)
        button_layout.addWidget(clear_btn)
        
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

    def setup_stats_tab(self):
        """Thiết lập tab thống kê"""
        layout = QVBoxLayout(self.stats_tab)
        
        # Statistics display
        self.stats_text = QTextEdit()
        self.stats_text.setReadOnly(True)
        self.stats_text.setMaximumHeight(200)
        layout.addWidget(self.stats_text)
        
        # Daily statistics list
        daily_label = QLabel(" Thống kê theo ngày:")
        daily_label.setStyleSheet("""
            QLabel {
                color: #00ff88;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        layout.addWidget(daily_label)
        
        self.daily_stats_list = QListWidget()
        layout.addWidget(self.daily_stats_list)
    
    def setup_history_tab(self):
        """Thiết lập tab lịch sử chi tiết"""
        layout = QHBoxLayout(self.history_tab)
        
        # Left side - Sessions list
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        sessions_label = QLabel("Các phiên trò chuyện:")
        sessions_label.setStyleSheet("""
            QLabel {
                color: #00ff88;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        left_layout.addWidget(sessions_label)
        
        self.sessions_list = QListWidget()
        self.sessions_list.itemClicked.connect(self.load_session_conversations)
        left_layout.addWidget(self.sessions_list)
        
        layout.addWidget(left_widget)
        
        # Right side - Conversation content
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        content_label = QLabel(" Nội dung trò chuyện:")
        content_label.setStyleSheet("""
            QLabel {
                color: #00ccff;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        right_layout.addWidget(content_label)
        
        self.conversation_text = QTextEdit()
        self.conversation_text.setReadOnly(True)
        right_layout.addWidget(self.conversation_text)
        
        layout.addWidget(right_widget)
    
    def load_statistics(self):
        """Tải thống kê"""
        try:
            # Use SqlService methods instead of direct database access
            total_stats = self.db.get_statistics(self.user_name)
            daily_stats = self.db.get_daily_statistics(self.user_name, 30)
            
            # Display total statistics
            stats_text = f""" Thống kê tổng quan:

• Tổng số cuộc trò chuyện: {total_stats[0]}
• Số ngày sử dụng: {total_stats[1]}
• Số phiên trò chuyện: {total_stats[2]}
• Trung bình mỗi ngày: {total_stats[0]/max(total_stats[1], 1):.1f} cuộc trò chuyện
"""
            
            self.stats_text.setPlainText(stats_text)
            
            # Display daily statistics
            self.daily_stats_list.clear()
            for date, conv_count, sess_count in daily_stats:
                item_text = f" {date}: {conv_count} câu hỏi, {sess_count} phiên"
                item = QListWidgetItem(item_text)
                self.daily_stats_list.addItem(item)
                
        except Exception as e:
            print(f"Error loading statistics: {e}")
    
    def load_session_conversations(self, item):
        """Tải nội dung cuộc trò chuyện của phiên được chọn"""
        try:
            # Get session_id safely
            if item is None:
                print("Warning: item is None")
                return
                
            session_id = item.data(Qt.ItemDataRole.UserRole)
            if session_id is None:
                print("Warning: session_id is None")
                return
                
            conversations = self.db.get_session_conversations(session_id)
            
            content = f" Phiên trò chuyện: {session_id}\n"
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
            import traceback
            traceback.print_exc()
            self.conversation_text.setPlainText("Lỗi khi tải cuộc trò chuyện")
    
    def refresh_data(self):
        """Làm mới dữ liệu"""
        self.load_statistics()
        self.load_sessions()
        print("Data refreshed")
    
    def load_sessions(self):
        """Tải danh sách phiên"""
        try:
            sessions = self.db.get_all_sessions(self.user_name)
            
            self.sessions_list.clear()
            
            for session in sessions:
                session_id, start_time, end_time = session
                start_str = start_time.replace('T', ' ')[:19] if start_time else "Unknown"
                end_str = end_time.replace('T', ' ')[:19] if end_time else "Đang hoạt động"
                
                item_text = f" {start_str} - {end_str}"
                item = QListWidgetItem(item_text)
                item.setData(Qt.ItemDataRole.UserRole, session_id)
                self.sessions_list.addItem(item)
                
        except Exception as e:
            print(f"Error loading sessions: {e}")
    
    def clear_old_data(self):
        """Xóa dữ liệu cũ"""
        try:
            self.db.delete_old_conversations(30)
            self.refresh_data()
            print("Old conversations deleted")
        except Exception as e:
            print(f"Error deleting old data: {e}")
