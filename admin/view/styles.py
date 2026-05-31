#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pop Assistant - Admin Panel Styles (Premium Redesign)
Glassmorphism + Neon Glow + Depth-focused Design System
"""

# ═══════════════════════════════════════════════════════════
# COLOR TOKENS
# ═══════════════════════════════════════════════════════════
ACCENT_PRIMARY = "#00ffaa"
ACCENT_SECONDARY = "#00ccff"
ACCENT_TERTIARY = "#a78bfa"  # Soft violet
BG_DARKEST = "#0d1017"
BG_DARK = "#141922"
BG_MEDIUM = "#1a2030"
BG_LIGHT = "#222b3a"
TEXT_PRIMARY = "#f0f2f5"
TEXT_SECONDARY = "#8b95a5"
TEXT_MUTED = "#5a6375"
BORDER_GLOW = "rgba(0, 255, 170, 0.25)"
BORDER_SUBTLE = "rgba(0, 255, 170, 0.12)"

# ═══════════════════════════════════════════════════════════
# MAIN WINDOW
# ═══════════════════════════════════════════════════════════
MAIN_WINDOW = f"""
QMainWindow {{
    background: qlineargradient(x1:0, y1:0, x2:0.3, y2:1,
                   stop:0 {BG_DARKEST}, stop:0.5 {BG_DARK}, stop:1 {BG_MEDIUM});
    color: {TEXT_PRIMARY};
}}
QWidget {{
    background-color: transparent;
    color: {TEXT_PRIMARY};
    font-family: 'Segoe UI', 'Inter', sans-serif;
}}
QLabel {{
    color: {TEXT_PRIMARY};
    font-family: 'Segoe UI', 'Inter', sans-serif;
}}
QTextEdit {{
    color: {TEXT_PRIMARY};
    font-family: 'Segoe UI', 'Inter', sans-serif;
}}
QScrollBar:vertical {{
    background: rgba(20, 25, 34, 0.6);
    width: 8px;
    margin: 0;
    border-radius: 4px;
}}
QScrollBar::handle:vertical {{
    background: rgba(0, 255, 170, 0.25);
    min-height: 30px;
    border-radius: 4px;
}}
QScrollBar::handle:vertical:hover {{
    background: rgba(0, 255, 170, 0.45);
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
QScrollBar:horizontal {{
    background: rgba(20, 25, 34, 0.6);
    height: 8px;
    margin: 0;
    border-radius: 4px;
}}
QScrollBar::handle:horizontal {{
    background: rgba(0, 255, 170, 0.25);
    min-width: 30px;
    border-radius: 4px;
}}
QScrollBar::handle:horizontal:hover {{
    background: rgba(0, 255, 170, 0.45);
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0;
}}
QScrollArea {{
    background: transparent;
    border: none;
}}
"""

# ═══════════════════════════════════════════════════════════
# TAB WIDGET — Premium Depth
# ═══════════════════════════════════════════════════════════
TAB_WIDGET = f"""
QTabWidget::pane {{
    border: 1px solid rgba(0, 255, 170, 0.15);
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                   stop:0 rgba(22, 30, 44, 0.95), stop:1 rgba(16, 22, 34, 0.98));
    border-radius: 16px;
    padding: 20px;
    margin-top: -1px;
}}
QTabBar::tab {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                   stop:0 rgba(30, 40, 56, 0.9), stop:1 rgba(22, 30, 44, 0.95));
    color: {TEXT_SECONDARY};
    padding: 14px 32px;
    margin-right: 3px;
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
    font-family: 'Segoe UI', sans-serif;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.3px;
    border: 1px solid rgba(0, 255, 170, 0.08);
    border-bottom: none;
    min-width: 130px;
}}
QTabBar::tab:selected {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                   stop:0 rgba(0, 255, 170, 0.15), stop:1 rgba(22, 30, 44, 0.95));
    color: #00ffaa;
    border: 1px solid rgba(0, 255, 170, 0.3);
    border-bottom: 3px solid #00ffaa;
}}
QTabBar::tab:hover:!selected {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                   stop:0 rgba(0, 255, 170, 0.08), stop:1 rgba(22, 30, 44, 0.9));
    color: {TEXT_PRIMARY};
    border: 1px solid rgba(0, 255, 170, 0.15);
    border-bottom: none;
}}
"""

# ═══════════════════════════════════════════════════════════
# HEADER — Glassmorphism + Neon accent
# ═══════════════════════════════════════════════════════════
HEADER_FRAME = f"""
QFrame {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0.5,
                   stop:0 rgba(0, 255, 170, 0.08), stop:0.5 rgba(0, 204, 255, 0.06), stop:1 rgba(167, 139, 250, 0.05));
    border: 1px solid rgba(0, 255, 170, 0.2);
    border-radius: 18px;
    padding: 18px 24px;
}}
"""

HEADER_TITLE = f"""
QLabel {{
    color: {ACCENT_PRIMARY};
    font-size: 26px;
    font-weight: 700;
    font-family: 'Segoe UI', sans-serif;
    letter-spacing: 1px;
    padding: 8px 12px;
}}
"""

HEADER_STATUS = f"""
QLabel {{
    color: #00ff88;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                   stop:0 rgba(0, 255, 136, 0.12), stop:1 rgba(0, 255, 136, 0.06));
    border: 1px solid rgba(0, 255, 136, 0.35);
    border-radius: 20px;
    padding: 8px 20px;
    font-size: 12px;
    font-family: 'Segoe UI', sans-serif;
    font-weight: 600;
    letter-spacing: 0.5px;
}}
"""

HEADER_TIME = f"""
QLabel {{
    color: {ACCENT_SECONDARY};
    font-size: 13px;
    font-family: 'Segoe UI', sans-serif;
    font-weight: 500;
    padding: 8px 12px;
    background: rgba(0, 204, 255, 0.06);
    border: 1px solid rgba(0, 204, 255, 0.15);
    border-radius: 10px;
}}
"""

# ═══════════════════════════════════════════════════════════
# FOOTER — Subtle bar
# ═══════════════════════════════════════════════════════════
FOOTER_FRAME = f"""
QFrame {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                   stop:0 rgba(0, 255, 170, 0.06), stop:1 rgba(0, 204, 255, 0.04));
    border: 1px solid rgba(0, 255, 170, 0.12);
    border-radius: 12px;
    padding: 10px 18px;
}}
"""

FOOTER_INFO = f"""
QLabel {{
    color: {TEXT_MUTED};
    font-size: 11px;
    font-family: 'Segoe UI', sans-serif;
    letter-spacing: 0.5px;
}}
"""

# ═══════════════════════════════════════════════════════════
# TABLE — Premium with depth + glow
# ═══════════════════════════════════════════════════════════
TABLE_WIDGET = f"""
QTableWidget {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                   stop:0 rgba(18, 24, 38, 0.98), stop:1 rgba(14, 18, 28, 0.99));
    border: 1px solid rgba(0, 255, 170, 0.15);
    border-radius: 12px;
    gridline-color: rgba(0, 255, 170, 0.06);
    color: {TEXT_PRIMARY};
    selection-background-color: rgba(0, 255, 170, 0.18);
    outline: none;
    font-size: 13px;
    font-family: 'Segoe UI', sans-serif;
}}
QTableWidget::item {{
    padding: 12px 16px;
    border-bottom: 1px solid rgba(0, 255, 170, 0.06);
    color: {TEXT_PRIMARY};
    background: transparent;
    font-size: 13px;
}}
QTableWidget::item:selected {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                   stop:0 rgba(0, 255, 170, 0.2), stop:1 rgba(0, 204, 255, 0.15));
    color: #ffffff;
    border: none;
}}
QTableWidget::item:hover {{
    background: rgba(0, 255, 170, 0.08);
}}
QHeaderView::section {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                   stop:0 rgba(0, 255, 170, 0.12), stop:1 rgba(0, 255, 170, 0.06));
    color: {ACCENT_PRIMARY};
    padding: 14px 16px;
    border: none;
    font-weight: 700;
    font-size: 12px;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    border-right: 1px solid rgba(0, 255, 170, 0.1);
    border-bottom: 2px solid rgba(0, 255, 170, 0.2);
}}
QHeaderView::section:last {{
    border-right: none;
}}
"""

# ═══════════════════════════════════════════════════════════
# BUTTONS — Depth + Glow + Pressed states
# ═══════════════════════════════════════════════════════════
def button_style(color1, color2, hover_color1=None, hover_color2=None, text_color="#ffffff"):
    """Generate premium gradient button style with depth"""
    if hover_color1 is None:
        hover_color1 = color1
        hover_color2 = color2
    return f"""
QPushButton {{
    padding: 11px 24px;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                   stop:0 {color1}, stop:1 {color2});
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    color: {text_color};
    font-size: 13px;
    font-weight: 600;
    font-family: 'Segoe UI', sans-serif;
    letter-spacing: 0.3px;
}}
QPushButton:hover {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                   stop:0 {hover_color1}, stop:1 {hover_color2});
    border: 1px solid rgba(255, 255, 255, 0.15);
}}
QPushButton:pressed {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                   stop:0 {color2}, stop:1 {color1});
    padding-top: 12px;
    padding-bottom: 10px;
}}
"""

# Predefined button styles
BUTTON_GREEN = button_style(
    "rgba(39, 174, 96, 0.85)", "rgba(27, 140, 75, 0.9)",
    "rgba(46, 204, 113, 0.95)", "rgba(39, 174, 96, 0.95)"
)

BUTTON_RED = button_style(
    "rgba(231, 76, 60, 0.85)", "rgba(192, 57, 43, 0.9)",
    "rgba(240, 96, 96, 0.95)", "rgba(231, 76, 60, 0.95)"
)

BUTTON_BLUE = button_style(
    "rgba(52, 152, 219, 0.85)", "rgba(41, 115, 185, 0.9)",
    "rgba(93, 173, 226, 0.95)", "rgba(52, 152, 219, 0.95)"
)

BUTTON_ORANGE = button_style(
    "rgba(243, 156, 18, 0.85)", "rgba(210, 126, 14, 0.9)",
    "rgba(241, 196, 15, 0.95)", "rgba(243, 156, 18, 0.95)"
)

BUTTON_PURPLE = button_style(
    "rgba(142, 100, 210, 0.85)", "rgba(120, 80, 190, 0.9)",
    "rgba(167, 139, 250, 0.95)", "rgba(142, 100, 210, 0.95)"
)

BUTTON_LOGOUT = f"""
QPushButton {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                   stop:0 rgba(231, 76, 60, 0.8), stop:1 rgba(180, 50, 35, 0.85));
    color: white;
    border: 1px solid rgba(231, 76, 60, 0.3);
    border-radius: 10px;
    padding: 10px 22px;
    font-size: 12px;
    font-family: 'Segoe UI', sans-serif;
    font-weight: 600;
    letter-spacing: 0.3px;
}}
QPushButton:hover {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                   stop:0 rgba(255, 107, 107, 0.9), stop:1 rgba(231, 76, 60, 0.9));
    border: 1px solid rgba(255, 107, 107, 0.4);
}}
"""

# ═══════════════════════════════════════════════════════════
# CARD / INFO FRAME — Glassmorphism
# ═══════════════════════════════════════════════════════════
INFO_FRAME = f"""
QFrame {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                   stop:0 rgba(52, 152, 219, 0.08), stop:1 rgba(52, 152, 219, 0.04));
    border: 1px solid rgba(52, 152, 219, 0.2);
    border-radius: 14px;
    padding: 18px;
}}
"""

INFO_LABEL = f"""
QLabel {{
    font-size: 14px;
    color: {TEXT_PRIMARY};
    padding: 8px;
    line-height: 1.6;
    font-family: 'Segoe UI', sans-serif;
}}
"""

LOG_TEXT = f"""
QTextEdit {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                   stop:0 rgba(8, 10, 18, 0.95), stop:1 rgba(12, 15, 24, 0.98));
    color: {ACCENT_PRIMARY};
    border: 1px solid rgba(0, 255, 170, 0.15);
    border-radius: 10px;
    padding: 12px;
    font-family: 'Cascadia Code', 'Consolas', 'Fira Code', monospace;
    font-size: 12px;
    selection-background-color: rgba(0, 255, 170, 0.2);
}}
"""

# ═══════════════════════════════════════════════════════════
# STATS CARD — Enhanced
# ═══════════════════════════════════════════════════════════
def stats_card_style(color):
    """Generate premium stats card style"""
    return f"""
QLabel {{
    font-size: 36px;
    font-weight: 700;
    color: {color};
    background: transparent;
    padding: 8px;
    text-align: center;
}}
"""

STATS_CARD_BLUE = stats_card_style("#3498db")
STATS_CARD_GREEN = stats_card_style("#27ae60")
STATS_CARD_ORANGE = stats_card_style("#f39c12")
STATS_CARD_RED = stats_card_style("#e74c3c")

# ═══════════════════════════════════════════════════════════
# GLASS CARD — Reusable glassmorphism card
# ═══════════════════════════════════════════════════════════
def glass_card(accent_color=ACCENT_PRIMARY, alpha=0.06):
    """Generate glassmorphism card style"""
    r, g, b = _hex_to_rgb(accent_color)
    return f"""
QFrame {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                   stop:0 rgba({r}, {g}, {b}, {alpha}),
                   stop:0.5 rgba({r}, {g}, {b}, {alpha * 0.5}),
                   stop:1 rgba({r}, {g}, {b}, {alpha * 0.3}));
    border: 1px solid rgba({r}, {g}, {b}, 0.18);
    border-radius: 14px;
    padding: 16px;
}}
QLabel {{
    color: {TEXT_PRIMARY};
    background: transparent;
    border: none;
}}
"""

def _hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 6:
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return (0, 255, 170)  # default accent

# ═══════════════════════════════════════════════════════════
# DIALOG — Premium dark glass
# ═══════════════════════════════════════════════════════════
DIALOG_MAIN = f"""
QDialog {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                   stop:0 {BG_DARKEST}, stop:1 {BG_DARK});
    color: {TEXT_PRIMARY};
}}
QLabel {{
    color: {TEXT_PRIMARY};
    font-size: 13px;
    font-family: 'Segoe UI', sans-serif;
}}
QLineEdit {{
    background: rgba(14, 18, 28, 0.9);
    border: 1px solid rgba(0, 255, 170, 0.2);
    border-radius: 10px;
    padding: 10px 14px;
    color: {TEXT_PRIMARY};
    font-size: 13px;
    font-family: 'Segoe UI', sans-serif;
}}
QLineEdit:focus {{
    border: 1px solid rgba(0, 255, 170, 0.5);
    background: rgba(14, 18, 28, 0.95);
}}
"""

DIALOG_CONVERSATION = f"""
QDialog {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                   stop:0 {BG_DARKEST}, stop:1 {BG_DARK});
    color: {ACCENT_PRIMARY};
}}
QLabel {{
    color: {TEXT_PRIMARY};
    font-size: 13px;
    padding: 4px;
    font-family: 'Segoe UI', sans-serif;
}}
QTextEdit {{
    background: rgba(10, 14, 22, 0.95);
    border: 1px solid rgba(0, 255, 170, 0.15);
    border-radius: 10px;
    padding: 12px;
    color: {TEXT_PRIMARY};
    font-size: 13px;
    font-family: 'Segoe UI', sans-serif;
}}
QPushButton {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                   stop:0 rgba(0, 255, 170, 0.2), stop:1 rgba(0, 204, 136, 0.25));
    color: {ACCENT_PRIMARY};
    border: 1px solid rgba(0, 255, 170, 0.3);
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 600;
    font-family: 'Segoe UI', sans-serif;
}}
QPushButton:hover {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                   stop:0 rgba(0, 255, 170, 0.3), stop:1 rgba(0, 204, 136, 0.35));
    border: 1px solid rgba(0, 255, 170, 0.5);
}}
QScrollArea {{
    background: transparent;
    border: none;
}}
QFrame {{
    background: rgba(18, 24, 38, 0.9);
    border: 1px solid rgba(0, 255, 170, 0.12);
    border-radius: 12px;
    padding: 12px;
    margin: 4px;
}}
"""

CONVERSATION_HEADER = f"""
QFrame {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                   stop:0 rgba(0, 255, 170, 0.08), stop:1 rgba(0, 204, 255, 0.05));
    border: 1px solid rgba(0, 255, 170, 0.2);
    border-radius: 12px;
    padding: 16px;
}}
"""

# ═══════════════════════════════════════════════════════════
# GROUP BOX — Premium section headers
# ═══════════════════════════════════════════════════════════
GROUP_BOX = f"""
QGroupBox {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                   stop:0 rgba(22, 30, 44, 0.7), stop:1 rgba(16, 22, 34, 0.8));
    border: 1px solid rgba(0, 255, 170, 0.1);
    border-radius: 14px;
    margin-top: 20px;
    padding: 20px 16px 16px 16px;
    font-family: 'Segoe UI', sans-serif;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 6px 16px;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                   stop:0 rgba(0, 255, 170, 0.15), stop:1 rgba(0, 204, 255, 0.1));
    border: 1px solid rgba(0, 255, 170, 0.2);
    border-radius: 8px;
    color: {ACCENT_PRIMARY};
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.5px;
}}
"""

# ═══════════════════════════════════════════════════════════
# PROGRESS BAR — Neon glow
# ═══════════════════════════════════════════════════════════
def progress_bar_style(color="#00ffaa"):
    """Generate premium progress bar style"""
    r, g, b = _hex_to_rgb(color)
    return f"""
QProgressBar {{
    background: rgba(14, 18, 28, 0.8);
    border: 1px solid rgba({r}, {g}, {b}, 0.2);
    border-radius: 8px;
    height: 18px;
    text-align: center;
    color: {TEXT_PRIMARY};
    font-size: 11px;
    font-weight: 600;
    font-family: 'Segoe UI', sans-serif;
}}
QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                   stop:0 rgba({r}, {g}, {b}, 0.7),
                   stop:0.5 rgba({r}, {g}, {b}, 0.9),
                   stop:1 rgba({r}, {g}, {b}, 0.7));
    border-radius: 7px;
}}
"""

PROGRESS_GREEN = progress_bar_style("#27ae60")
PROGRESS_YELLOW = progress_bar_style("#f39c12")
PROGRESS_RED = progress_bar_style("#e74c3c")

# ═══════════════════════════════════════════════════════════
# COMBOBOX — Premium dropdown
# ═══════════════════════════════════════════════════════════
COMBO_BOX = f"""
QComboBox {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                   stop:0 rgba(22, 30, 44, 0.95), stop:1 rgba(16, 22, 34, 0.98));
    border: 1px solid rgba(0, 255, 170, 0.2);
    border-radius: 10px;
    padding: 10px 16px;
    color: {TEXT_PRIMARY};
    font-size: 13px;
    font-family: 'Segoe UI', sans-serif;
    min-height: 18px;
}}
QComboBox:hover {{
    border: 1px solid rgba(0, 255, 170, 0.4);
}}
QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: center right;
    width: 30px;
    border-left: 1px solid rgba(0, 255, 170, 0.1);
    border-top-right-radius: 10px;
    border-bottom-right-radius: 10px;
}}
QComboBox::down-arrow {{
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid rgba(0, 255, 170, 0.6);
    margin-right: 8px;
}}
QComboBox QAbstractItemView {{
    background: rgba(16, 22, 34, 0.98);
    border: 1px solid rgba(0, 255, 170, 0.2);
    border-radius: 8px;
    color: {TEXT_PRIMARY};
    selection-background-color: rgba(0, 255, 170, 0.15);
    selection-color: {ACCENT_PRIMARY};
    padding: 4px;
    outline: none;
}}
QComboBox QAbstractItemView::item {{
    padding: 8px 12px;
    min-height: 28px;
    border-radius: 6px;
}}
QComboBox QAbstractItemView::item:hover {{
    background: rgba(0, 255, 170, 0.1);
}}
"""

# ═══════════════════════════════════════════════════════════
# ONLINE STATUS BADGE
# ═══════════════════════════════════════════════════════════
ONLINE_BADGE = f"""
QLabel {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                   stop:0 rgba(0, 255, 170, 0.08), stop:1 rgba(0, 204, 255, 0.06));
    border: 1px solid rgba(0, 255, 170, 0.2);
    border-radius: 20px;
    padding: 8px 20px;
    font-size: 13px;
    font-weight: 600;
    color: {TEXT_PRIMARY};
    font-family: 'Segoe UI', sans-serif;
    letter-spacing: 0.3px;
}}
"""

# ═══════════════════════════════════════════════════════════
# SECTION TITLE — For tab section headers
# ═══════════════════════════════════════════════════════════
SECTION_TITLE = f"""
QLabel {{
    color: {ACCENT_PRIMARY};
    font-size: 18px;
    font-weight: 700;
    font-family: 'Segoe UI', sans-serif;
    letter-spacing: 0.5px;
    padding: 4px 0px;
    border: none;
    background: transparent;
}}
"""

SECTION_SUBTITLE = f"""
QLabel {{
    color: {TEXT_MUTED};
    font-size: 12px;
    font-weight: 400;
    font-family: 'Segoe UI', sans-serif;
    letter-spacing: 0.3px;
    padding: 0px;
    border: none;
    background: transparent;
}}
"""

# ═══════════════════════════════════════════════════════════
# CARD FRAME — For health tab metric cards etc.
# ═══════════════════════════════════════════════════════════
CARD_FRAME = f"""
QFrame {{
    background: qlineargradient(x1:0, y1:0, x2:0.5, y2:1,
                   stop:0 rgba(255, 255, 255, 0.05), stop:1 rgba(255, 255, 255, 0.02));
    border: 1px solid rgba(0, 255, 170, 0.12);
    border-radius: 14px;
    padding: 14px;
}}
QLabel {{
    color: {TEXT_PRIMARY};
    background: transparent;
    border: none;
}}
"""

# ═══════════════════════════════════════════════════════════
# SEPARATOR LINE
# ═══════════════════════════════════════════════════════════
SEPARATOR = f"""
QFrame {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                   stop:0 transparent, stop:0.5 rgba(0, 255, 170, 0.2), stop:1 transparent);
    max-height: 1px;
    min-height: 1px;
    border: none;
}}
"""
