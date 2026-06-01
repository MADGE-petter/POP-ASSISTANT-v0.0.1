"""
dialogs.py — Compatibility shim.

File này chỉ re-export các lớp từ các module riêng biệt.
Để debug hoặc chỉnh sửa, hãy mở trực tiếp file tương ứng:

  base_dialog.py          → FooterDialog
  settings_dialog.py      → SettingsDialog
  audio_dialog.py         → AudioDialog
  personal_info_dialog.py → PersonalInfoDialog
  history_usage_dialog.py → HistoryUsageDialog
"""

from view.widgets.audio_dialog import AudioDialog  # noqa: F401
from view.widgets.base_dialog import FooterDialog  # noqa: F401
from view.widgets.history_usage_dialog import HistoryUsageDialog  # noqa: F401
from view.widgets.personal_info_dialog import PersonalInfoDialog  # noqa: F401
from view.widgets.settings_dialog import SettingsDialog  # noqa: F401

__all__ = [
    'FooterDialog',
    'SettingsDialog',
    'AudioDialog',
    'PersonalInfoDialog',
    'HistoryUsageDialog',
]
