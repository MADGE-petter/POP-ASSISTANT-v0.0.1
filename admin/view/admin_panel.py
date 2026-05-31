"""
Pop Assistant - Admin Panel (Premium Redesign)
Giao diện quản trị admin - Refactored MVC
"""

import os
import sys
from datetime import datetime
if __package__ is None and __name__ == "__main__":
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from admin.controller.admin_controller import AdminController

# Avoid manipulating sys.path; use package imports
from admin.model.admin_model import AdminModel
from admin.view.styles import (
    BUTTON_LOGOUT,
    FOOTER_FRAME,
    FOOTER_INFO,
    HEADER_FRAME,
    HEADER_STATUS,
    HEADER_TIME,
    HEADER_TITLE,
    MAIN_WINDOW,
    SEPARATOR,
    TAB_WIDGET,
)
from admin.view.tabs import ConversationsTab, DatabaseTab, HealthTab, StatsTab, UsersTab
from view.ui_helpers import create_ui_footer


class AdminPanel(QMainWindow):
    """Admin Panel Interface - Container chính"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pop Assistant - Admin Panel")
        self.setGeometry(100, 100, 1280, 860)
        
        # Initialize MVC components
        self.admin_model = AdminModel()
        self.admin_controller = AdminController()
        
        # Connect signals
        self.admin_controller.data_updated.connect(self.on_data_updated)
        self.admin_controller.error_occurred.connect(self.on_error_occurred)
        
        # Apply styles
        self.setStyleSheet(MAIN_WINDOW)
        
        # Setup UI
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """Setup main UI structure"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(26, 24, 26, 20)
        layout.setSpacing(20)
        
        # Header
        self.create_header(layout)
        
        # Separator line
        sep = QFrame()
        sep.setStyleSheet(SEPARATOR)
        sep.setFixedHeight(1)
        layout.addWidget(sep)
        
        # Tab Widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(TAB_WIDGET)
        self.tab_widget.setDocumentMode(False)
        self.tab_widget.setUsesScrollButtons(True)
        self.tab_widget.tabBar().setExpanding(False)
        self.tab_widget.tabBar().setElideMode(Qt.TextElideMode.ElideRight)
        self.create_tabs()
        layout.addWidget(self.tab_widget, 1)  # stretch factor 1 - takes remaining space
        
        # Footer
        self.create_footer(layout)
    
    def create_header(self, layout):
        """Create header section"""
        header_frame = QFrame()
        header_frame.setStyleSheet(HEADER_FRAME)
        
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(16, 8, 16, 8)
        header_layout.setSpacing(16)
        
        # Title area
        title_area = QVBoxLayout()
        title_area.setSpacing(2)
        
        title_label = QLabel("POP ASSISTANT ADMIN PANEL")
        title_label.setStyleSheet(HEADER_TITLE)
        title_area.addWidget(title_label)
        
        subtitle_label = QLabel("Design by Madge| Tuan Nguyen")
        subtitle_label.setStyleSheet("""
            QLabel {
                color: rgba(139, 149, 165, 0.8);
                font-size: 12px;
                font-weight: 400;
                font-family: 'Segoe UI', sans-serif;
                letter-spacing: 0.5px;
                padding: 0px 12px;
            }
        """)
        title_area.addWidget(subtitle_label)
        
        header_layout.addLayout(title_area)
        header_layout.addStretch()
        
        # Status badge
        self.status_label = QLabel("● System Online")
        self.status_label.setStyleSheet(HEADER_STATUS)
        header_layout.addWidget(self.status_label)
        
        # Time
        self.time_label = QLabel()
        self.time_label.setStyleSheet(HEADER_TIME)
        self.update_time()
        
        # Update timer
        self.time_timer = QTimer()
        self.time_timer.timeout.connect(self.update_time)
        self.time_timer.start(1000)
        
        header_layout.addWidget(self.time_label)
        layout.addWidget(header_frame)
    
    def create_tabs(self):
        """Create all tabs"""
        # Users Tab
        self.users_tab = UsersTab(log_callback=self.log_message)
        self.tab_widget.addTab(self.users_tab, "Quản lý Users")
        
        # Health Tab
        self.health_tab = HealthTab(log_callback=self.log_message)
        self.tab_widget.addTab(self.health_tab, "Sức khỏe")
        
        # Database Tab
        self.database_tab = DatabaseTab(log_callback=self.log_message)
        self.tab_widget.addTab(self.database_tab, "Quản lý Database")
        
        # Stats Tab
        self.stats_tab = StatsTab(log_callback=self.log_message)
        self.tab_widget.addTab(self.stats_tab, "Thống kê")
        
        # Conversations Tab
        self.conversations_tab = ConversationsTab(log_callback=self.log_message)
        self.tab_widget.addTab(self.conversations_tab, "Trò Chuyện")
    
    def create_footer(self, layout):
        """Create footer section"""
        footer_frame = QFrame()
        footer_frame.setStyleSheet(FOOTER_FRAME)
        
        footer_layout = QHBoxLayout(footer_frame)
        footer_layout.setContentsMargins(12, 6, 12, 6)
        
        # Info label
        info_label = QLabel("Pop Assistant Admin Panel v1.0  •  Made with ♥")
        info_label.setStyleSheet(FOOTER_INFO)
        footer_layout.addWidget(info_label)
        
        footer_layout.addStretch()
        
        # Logout button
        logout_btn = QPushButton("⏻  Logout")
        logout_btn.setStyleSheet(BUTTON_LOGOUT)
        logout_btn.clicked.connect(self.close)
        footer_layout.addWidget(logout_btn)
        
        layout.addWidget(footer_frame)
    
    def update_time(self):
        """Update time display"""
        current_time = datetime.now().strftime("%H:%M:%S  •  %d/%m/%Y")
        self.time_label.setText(f" {current_time}")
    
    def log_message(self, message):
        """Log message to database tab"""
        if hasattr(self, 'database_tab') and self.database_tab:
            self.database_tab.log_message(message)
        else:
            print(f"[AdminPanel] {message}")
    
    def load_data(self):
        """Load initial data"""
        self.refresh_data()
    
    def refresh_data(self):
        """Refresh all data via controller"""
        try:
            self.admin_controller.get_dashboard_data()
            self.admin_controller.get_user_management_data()
            self.admin_controller.get_conversation_history_data()
            self.log_message("Data refreshed successfully")
        except Exception as e:
            self.log_message(f"Error refreshing data: {e}")
    
    def on_data_updated(self, data_type, data):
        """Handle data updated signals"""
        if data_type == 'dashboard':
            self.update_dashboard(data)
        elif data_type == 'user_management':
            self.update_user_management(data)
        elif data_type == 'conversation_history':
            self.update_conversations(data)
    
    def on_error_occurred(self, error_message):
        """Handle error signals"""
        QMessageBox.warning(self, "Lỗi", error_message)
        self.log_message(f"Error: {error_message}")
    
    def update_dashboard(self, data):
        """Update dashboard with data from controller"""
        stats = data.get('user_statistics', {})
        if stats:
            self.stats_tab.total_users_card.set_value(str(stats.get('total_users', 0)))
            self.stats_tab.total_conversations_card.set_value(str(stats.get('total_conversations', 0)))
            active = stats.get('active_users_7d', 0) or stats.get('total_sessions', 0)
            self.stats_tab.active_sessions_card.set_value(str(active))
    
    def update_user_management(self, data):
        """Update user management data"""
        pass  # Tab tự quản lý data
    
    def update_conversations(self, data):
        """Update conversation data"""
        pass  # Tab tự quản lý data
    
    def closeEvent(self, event):
        """Handle window close"""
        reply = QMessageBox.question(
            self, "Xác nhận", "Bạn có chắc muốn thoát Admin Panel?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            app = QApplication.instance()
            if app:
                app.quit()
            event.accept()
        else:
            event.ignore()


def create_admin_panel():
    """Create admin panel window"""
    return AdminPanel()


def main():
    """Main function"""
    app = QApplication(sys.argv)
    app.setApplicationName("Pop Assistant Admin Panel")
    app.setOrganizationName("Pop AI")
    
    admin_panel = AdminPanel()
    admin_panel.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
