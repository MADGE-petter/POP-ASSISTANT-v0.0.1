#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pop Assistant - Admin Controller
Điều phối logic cho admin panel theo pattern MVC
"""

import os
from datetime import datetime
from typing import Callable, Dict, List, Optional

from PyQt6.QtCore import QObject, pyqtSignal

# Import model
from admin.model.admin_model import AdminModel


class AdminController(QObject):
    """Controller layer cho Admin Panel - điều phối giữa Model và View"""
    
    # Signals để thông báo cho View
    login_success = pyqtSignal(dict)
    login_failed = pyqtSignal(str)
    data_updated = pyqtSignal(str, object)
    error_occurred = pyqtSignal(str)
    
    def __init__(self):
        """Khởi tạo AdminController"""
        super().__init__()
        self.model = AdminModel()
        self.current_admin = None
        self._callbacks = {}
    
    def register_callback(self, event: str, callback: Callable):
       
        self._callbacks[event] = callback
    
    def login_admin(self, username: str, password: str) -> bool:
        
        try:
            admin_data = self.model.verify_admin_login(username, password)
            
            if admin_data:
                self.current_admin = admin_data
                self.login_success.emit(admin_data)
                
                # Gọi callback nếu có
                if 'login_success' in self._callbacks:
                    self._callbacks['login_success'](admin_data)
                
                return True
            else:
                error_msg = "Tên đăng nhập hoặc mật khẩu không đúng"
                self.login_failed.emit(error_msg)
                
                # Gọi callback nếu có
                if 'login_failed' in self._callbacks:
                    self._callbacks['login_failed'](error_msg)
                
                return False
                
        except Exception as e:
            error_msg = f"Lỗi đăng nhập: {str(e)}"
            self.error_occurred.emit(error_msg)
            return False
    
    def get_dashboard_data(self) -> Dict:
        
        try:
            # Lấy thống kê người dùng
            user_stats = self.model.get_user_statistics()
            
            # Lấy conversations gần đây
            recent_conversations = self.model.get_conversation_history(limit=5)
            
            dashboard_data = {
                'user_statistics': user_stats,
                'recent_conversations': recent_conversations,
                'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Thông báo View
            self.data_updated.emit('dashboard', dashboard_data)
            
            return dashboard_data
            
        except Exception as e:
            error_msg = f"Lỗi lấy dữ liệu dashboard: {str(e)}"
            self.error_occurred.emit(error_msg)
            return {}
    
    def get_user_management_data(self) -> Dict:
        
        try:
            conversations = self.model.get_conversation_history(limit=1000)
            
            # Handle None or empty result
            if conversations is None:
                conversations = []
            
            # Group by user
            user_data = {}
            for conv in conversations:
                username = conv.get('user_name', 'Unknown')
                if username not in user_data:
                    user_data[username] = {
                        'conversation_count': 0,
                        'last_active': conv.get('created_at', ''),
                        'sessions': set()
                    }
                user_data[username]['conversation_count'] += 1
                user_data[username]['sessions'].add(conv.get('session_id', ''))
            
            # Chuyển sets sang counts
            for data in user_data.values():
                data['total_sessions'] = len(data['sessions'])
                del data['sessions']
            
            user_management_data = {
                'users': list(user_data.values()),
                'total_users': len(user_data),
                'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Thông báo View
            self.data_updated.emit('user_management', user_management_data)
            
            return user_management_data
            
        except Exception as e:
            error_msg = f"Lỗi lấy dữ liệu người dùng: {str(e)}"
            self.error_occurred.emit(error_msg)
            return {}
    
    def get_conversation_history_data(self, page: int = 1, page_size: int = 50, 
                                    user_filter: str = None, date_filter: str = None) -> Dict:
        
        try:
            offset = (page - 1) * page_size
            conversations = self.model.get_conversation_history(limit=page_size, offset=offset)
            
            # Áp dụng filter nếu có
            if user_filter:
                conversations = [c for c in conversations if user_filter.lower() in c['user_name'].lower()]
            
            if date_filter:
                conversations = [c for c in conversations if date_filter in c['created_at']]
            
            # Lấy danh sách users cho filter dropdown
            users = set()
            for conv in conversations:
                users.add(conv['user_name'])
            
            conversation_data = {
                'conversations': conversations,
                'users': sorted(list(users)),
                'current_page': page,
                'page_size': page_size,
                'total_conversations': len(conversations),
                'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Thông báo View
            self.data_updated.emit('conversation_history', conversation_data)
            
            return conversation_data
            
        except Exception as e:
            error_msg = f"Lỗi lấy lịch sử trò chuyện: {str(e)}"
            self.error_occurred.emit(error_msg)
            return {}
    
    
    
    
    def export_data(self, data_type: str, start_date: str = None, end_date: str = None) -> Optional[str]:
        
        try:
            filepath = self.model.export_data(data_type, start_date, end_date)
            
            if filepath:
                # Thông báo View
                self.data_updated.emit('data_exported', {'type': data_type, 'filepath': filepath})
                
                return filepath
            else:
                return None
                
        except Exception as e:
            error_msg = f"Lỗi export dữ liệu: {str(e)}"
            self.error_occurred.emit(error_msg)
            return None
    
    def cleanup_old_data(self, days: int = 30) -> int:
       
        try:
            deleted_count = self.model.cleanup_old_data(days)
            
            # Thông báo View
            self.data_updated.emit('data_cleaned', {'days': days, 'deleted_count': deleted_count})
            
            return deleted_count
            
        except Exception as e:
            error_msg = f"Lỗi dọn dẹp dữ liệu: {str(e)}"
            self.error_occurred.emit(error_msg)
            return 0
    
    def logout(self):
        self.current_admin = None
    
    def get_current_admin(self) -> Optional[Dict]:
        
        return self.current_admin
    
    def is_logged_in(self) -> bool:
        return self.current_admin is not None
