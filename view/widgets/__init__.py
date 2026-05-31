"""
Widgets package for Pop Assistant
Contains custom dialogs and windows
"""

from .dashboard_dialog import DashboardDialog
from .dialogs import AudioDialog, HistoryUsageDialog, PersonalInfoDialog, SettingsDialog
from .history_window import HistoryWindow

__all__ = [
    'HistoryWindow',
    'SettingsDialog',
    'AudioDialog',
    'PersonalInfoDialog',
    'HistoryUsageDialog',
    'DashboardDialog'
]
