from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel

DEFAULT_FOOTER_TEXT = "Design by Madge | Tuan Nguyen"
DEFAULT_FOOTER_COLOR = "#00ffcc"
DEFAULT_FOOTER_MARGIN = 20
DEFAULT_FOOTER_CORNER = "bottom_left"


def create_ui_footer(parent, text=DEFAULT_FOOTER_TEXT, color=DEFAULT_FOOTER_COLOR,
                     corner=DEFAULT_FOOTER_CORNER, margin=DEFAULT_FOOTER_MARGIN):
    """Tạo nhãn footer cố định cho một cửa sổ hoặc dialog."""
    footer_label = QLabel(text, parent)
    footer_label.setStyleSheet(f"""
        QLabel {{
            color: {color};
            font-size: 12px;
            font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
            font-weight: 500;
        }}
    """)
    footer_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
    footer_label.setAlignment(Qt.AlignmentFlag.AlignLeft if corner.endswith("left") else Qt.AlignmentFlag.AlignRight)
    footer_label.adjustSize()

    if not hasattr(parent, '_brand_footer_items'):
        parent._brand_footer_items = []
    parent._brand_footer_items.append((footer_label, corner, margin))
    position_ui_footer(parent)
    return footer_label


def position_ui_footer(parent):
    """Cập nhật vị trí footer khi kích thước parent thay đổi."""
    if not hasattr(parent, '_brand_footer_items'):
        return

    for footer_label, corner, margin in parent._brand_footer_items:
        footer_label.adjustSize()

        x = margin if corner.endswith('left') else max(margin, parent.width() - footer_label.width() - margin)
        y = margin if corner.startswith('top') else max(margin, parent.height() - footer_label.height() - margin)

        footer_label.move(x, y)
        footer_label.raise_()
