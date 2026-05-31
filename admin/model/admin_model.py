#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pop Assistant - Admin Model
Quản lý dữ liệu và business logic cho admin panel
"""

import csv
import hashlib
import os
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from database.admin_repository import AdminRepository
from utils.logger import get_logger

logger = get_logger(__name__)


class AdminModel:
    """Model layer cho Admin Panel - quản lý dữ liệu và business logic"""
    
    def __init__(self, db_path: str = None):
        """Khởi tạo AdminModel - delegate to AdminRepository."""
        if db_path is None:
            db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'database', 'conversations.db')
        
        self.db_path = db_path
        self.admin_repo = AdminRepository(db_path)
    

    
    def verify_admin_login(self, username: str, password: str) -> Optional[Dict]:
        """Xác thực admin login."""
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        result = self.admin_repo.verify_admin_login(username, password_hash)
        
        if result:
            self.admin_repo.add_system_log('INFO', f'Admin {username} đăng nhập thành công', 'AUTH')
        else:
            self.admin_repo.add_system_log('WARNING', f'Đăng nhập thất bại: {username}', 'AUTH')
        
        return result
    
    def get_user_statistics(self) -> Dict:
        """Lấy thống kê người dùng."""
        return self.admin_repo.get_user_statistics()
    
    def get_conversation_history(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Lấy lịch sử trò chuyện."""
        return self.admin_repo.get_conversation_history(limit, offset)
    
    def export_data(self, data_type: str, start_date: str = None, end_date: str = None) -> str:
        """Export dữ liệu theo type."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{data_type}_export_{timestamp}.csv"
            filepath = os.path.join(os.path.dirname(__file__), '..', '..', 'exports', filename)
            
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Lấy dữ liệu từ repository
            if data_type == 'conversations':
                data = self.admin_repo.export_conversations(start_date, end_date)
                headers = ['User', 'User Input', 'Bot Response', 'Created At', 'Session ID']
            elif data_type == 'users':
                data = self.admin_repo.export_users()
                headers = ['User Name', 'Created At', 'Last Interaction', 'Total Interactions']
            elif data_type == 'logs':
                data = self.admin_repo.export_logs(start_date, end_date)
                headers = ['Level', 'Message', 'Module', 'Created At']
            else:
                data = []
                headers = []
            
            # Ghi vào CSV
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(headers)
                writer.writerows(data)
            
            self.admin_repo.add_system_log('INFO', f'Export dữ liệu: {data_type} -> {filename}', 'EXPORT')
            
            return filepath
            
        except Exception as e:
            logger.error("Error exporting data: %s", e, exc_info=True)
            return None
    
    def cleanup_old_data(self, days: int = 30) -> int:
        """Dọn dẹp dữ liệu cũ."""
        deleted = self.admin_repo.cleanup_old_data(days)
        self.admin_repo.add_system_log('INFO', f'Dọn dẹp dữ liệu cũ: xóa {deleted} bản ghi', 'CLEANUP')
        return deleted

    def add_system_log(self, level: str, message: str, module: str) -> bool:
        """Thêm system log."""
        return self.admin_repo.add_system_log(level, message, module)
