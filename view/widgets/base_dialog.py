"""
Base dialog class for Pop Assistant dialogs.
"""
from PyQt6.QtWidgets import QDialog

from view.ui_helpers import position_ui_footer


class FooterDialog(QDialog):
    """Base class for all dialogs that use a footer watermark."""

    def resizeEvent(self, event):
        super().resizeEvent(event)
        position_ui_footer(self)
