#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Base class cho các Admin Tab - Giảm duplicate code"""

import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QPushButton,
    QTableWidget,
    QVBoxLayout,
    QWidget,
)


class BaseTab(QWidget):
    """Base class cho các tab trong Admin Panel"""
    
    DB_PATH = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', '..', '..', 'database', 'conversations.db'
    ))
    
    def __init__(self, parent=None, log_callback=None):
        super().__init__(parent)
        self.log_callback = log_callback or print
        self.db_path = self.DB_PATH
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """Override ở subclass"""
        pass
    
    def load_data(self):
        """Override ở subclass"""
        pass
    
    def create_table(self, columns, headers, style):
        """Tạo table chuẩn"""
        table = QTableWidget()
        table.setColumnCount(columns)
        table.setHorizontalHeaderLabels(headers)
        table.setStyleSheet(style)
        table.horizontalHeader().setStretchLastSection(True)
        from PyQt6.QtWidgets import QHeaderView
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setDefaultSectionSize(50)
        table.verticalHeader().setMinimumSectionSize(40)
        return table
    
    def create_button_frame(self, buttons):
        """Tạo button frame với list buttons [(text, style, callback)]"""
        frame = QFrame()
        layout = QHBoxLayout(frame)
        for text, style, callback in buttons:
            btn = QPushButton(text)
            btn.setStyleSheet(style)
            btn.clicked.connect(callback)
            layout.addWidget(btn)
        layout.addStretch()
        return frame
    
    def log(self, message):
        """Log message"""
        self.log_callback(f"[{self.__class__.__name__}] {message}")
