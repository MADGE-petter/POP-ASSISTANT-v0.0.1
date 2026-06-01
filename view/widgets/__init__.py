"""
Widgets package for Pop Assistant.

Dialog classes đã được tách ra từng file riêng để dễ bảo trì:
  base_dialog.py          — FooterDialog (base class)
  settings_dialog.py      — SettingsDialog
  audio_dialog.py         — AudioDialog
  personal_info_dialog.py — PersonalInfoDialog
  history_usage_dialog.py — HistoryUsageDialog
  history_window.py       — HistoryWindow
"""

from .audio_dialog import AudioDialog
from .base_dialog import FooterDialog
from .history_usage_dialog import HistoryUsageDialog
from .history_window import HistoryWindow
from .personal_info_dialog import PersonalInfoDialog
from .settings_dialog import SettingsDialog

__all__ = [
    'FooterDialog',
    'SettingsDialog',
    'AudioDialog',
    'PersonalInfoDialog',
    'HistoryUsageDialog',
    'HistoryWindow',
]
