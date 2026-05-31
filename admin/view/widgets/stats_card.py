#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pop Assistant - Stats Card Widget (Premium Redesign)
Glassmorphism card với accent glow, icon support, hover effect
"""

from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtWidgets import QFrame, QGraphicsDropShadowEffect, QLabel, QVBoxLayout


class StatsCard(QFrame):
    """Premium stats card widget với glassmorphism + neon glow"""

    def __init__(self, title, color, icon="", parent=None):
        super().__init__(parent)
        self.title = title
        self.color = color
        self.icon = icon
        self._hovered = False
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setMinimumHeight(130)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setup_ui()

    def setup_ui(self):
        r, g, b = self._hex_to_rgb(self.color)

        # Glassmorphism card style
        self.default_style = f"""
            QFrame#statsCard {{
                background: qlineargradient(x1:0, y1:0, x2:0.5, y2:1,
                               stop:0 rgba({r}, {g}, {b}, 0.1),
                               stop:0.5 rgba({r}, {g}, {b}, 0.05),
                               stop:1 rgba({r}, {g}, {b}, 0.02));
                border: 1px solid rgba({r}, {g}, {b}, 0.25);
                border-radius: 16px;
                padding: 0px;
            }}
        """
        self.hover_style = f"""
            QFrame#statsCard {{
                background: qlineargradient(x1:0, y1:0, x2:0.5, y2:1,
                               stop:0 rgba({r}, {g}, {b}, 0.18),
                               stop:0.5 rgba({r}, {g}, {b}, 0.1),
                               stop:1 rgba({r}, {g}, {b}, 0.05));
                border: 1px solid rgba({r}, {g}, {b}, 0.4);
                border-radius: 16px;
                padding: 0px;
            }}
        """
        self.setObjectName("statsCard")
        self.setStyleSheet(self.default_style)

        layout = QVBoxLayout(self)
        layout.setSpacing(6)
        layout.setContentsMargins(16, 18, 16, 14)

        # Top accent bar
        accent_bar = QFrame()
        accent_bar.setFixedHeight(3)
        accent_bar.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                               stop:0 {self.color}, stop:1 transparent);
                border-radius: 1px;
                border: none;
                margin: 0px;
                padding: 0px;
            }}
        """)
        layout.addWidget(accent_bar)

        # Title label
        self.title_label = QLabel(self.title)
        self.title_label.setStyleSheet(f"""
            QLabel {{
                font-size: 12px;
                color: rgba(180, 195, 215, 0.85);
                font-weight: 500;
                letter-spacing: 0.3px;
                font-family: 'Segoe UI', sans-serif;
                padding: 0px;
                background: transparent;
                border: none;
            }}
        """)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.title_label)

        # Value label
        self.value_label = QLabel("0")
        self.value_label.setStyleSheet(f"""
            QLabel {{
                font-size: 32px;
                font-weight: 700;
                color: {self.color};
                padding: 2px 0px;
                font-family: 'Segoe UI', sans-serif;
                background: transparent;
                border: none;
            }}
        """)
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.value_label)

        layout.addStretch()

    def set_value(self, value):
        """Cập nhật giá trị hiển thị"""
        self.value_label.setText(str(value))

    def enterEvent(self, event):
        """Hover in - glow effect"""
        self._hovered = True
        self.setStyleSheet(self.hover_style)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Hover out - reset"""
        self._hovered = False
        self.setStyleSheet(self.default_style)
        super().leaveEvent(event)

    @staticmethod
    def _hex_to_rgb(hex_color):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 6:
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return (0, 255, 170)
