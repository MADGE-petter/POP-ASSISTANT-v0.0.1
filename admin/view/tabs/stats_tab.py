#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pop Assistant - Stats Tab
Tab thống kê cơ bản
"""

import os

from database.admin_repository import AdminRepository
from utils.logger import get_logger

logger = get_logger(__name__)
from PyQt6.QtWidgets import QGridLayout, QGroupBox, QPushButton, QVBoxLayout

from admin.view.styles import BUTTON_BLUE
from admin.view.tabs.base_tab import BaseTab
from admin.view.widgets.stats_card import StatsCard


class StatsTab(BaseTab):
    """Tab thống kê"""
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # === Basic Statistics Only ===
        basic_frame = QGroupBox(" Thống kê cơ bản")
        basic_layout = QGridLayout(basic_frame)
        
        self.total_users_card = StatsCard("Tổng Users:", "#3498db")
        basic_layout.addWidget(self.total_users_card, 0, 0)
        
        self.total_conversations_card = StatsCard("Tổng Cuộc trò chuyện:", "#27ae60")
        basic_layout.addWidget(self.total_conversations_card, 0, 1)
        
        self.active_sessions_card = StatsCard("Phiên đang hoạt động:", "#f39c12")
        basic_layout.addWidget(self.active_sessions_card, 0, 2)
        
        self.db_size_card = StatsCard("Kích thước DB:", "#e74c3c")
        basic_layout.addWidget(self.db_size_card, 0, 3)
        
        # Additional stats row
        self.total_apps_card = StatsCard("Tổng App đã mở:", "#9b59b6")
        basic_layout.addWidget(self.total_apps_card, 1, 0)
        
        self.avg_session_card = StatsCard("Thời gian TB/phiên:", "#1abc9c")
        basic_layout.addWidget(self.avg_session_card, 1, 1)
        
        self.total_intents_card = StatsCard("Tổng Intent xử lý:", "#e67e22")
        basic_layout.addWidget(self.total_intents_card, 1, 2)
        
        self.error_rate_card = StatsCard("Tỷ lệ lỗi:", "#34495e")
        basic_layout.addWidget(self.error_rate_card, 1, 3)
        
        layout.addWidget(basic_frame)
        
        # Refresh button
        refresh_stats_btn = QPushButton("🔄 Làm mới thống kê")
        refresh_stats_btn.setStyleSheet(BUTTON_BLUE)
        refresh_stats_btn.clicked.connect(self.load_data)
        layout.addWidget(refresh_stats_btn)
        
        layout.addStretch()
    
    def load_data(self):
        """Load basic statistics"""
        try:
            self._load_basic_stats()
            self.log("Statistics refreshed")
        except Exception as e:
            self.log(f"Error: {e}")
    
    def _load_basic_stats(self):
        """Load basic database statistics"""
        total_users = total_conversations = active_sessions = 0
        total_apps = 0
        db_size_mb = 0.0
        
        if not os.path.exists(self.db_path):
            self.log("Database not found")
            return

        repo = AdminRepository(self.db_path)
        stats = repo.get_user_statistics()
        total_users = stats.get('total_users', 0)
        total_conversations = stats.get('total_conversations', 0)
        active_sessions = repo.get_active_sessions_count()
        total_apps = repo.get_app_usage_logs_count()
        
        size = os.path.getsize(self.db_path)
        db_size_mb = size / (1024 * 1024)
        
        self.total_users_card.set_value(str(total_users))
        self.total_conversations_card.set_value(str(total_conversations))
        self.active_sessions_card.set_value(str(active_sessions))
        self.db_size_card.set_value(f"{db_size_mb:.2f} MB")
        self.total_apps_card.set_value(str(total_apps))
        self.avg_session_card.set_value("-- min")
        self.total_intents_card.set_value("--")
        self.error_rate_card.set_value("--%")
