"""
PersonalInfoDialog — Dialog thông tin cá nhân & hiệu suất hệ thống.
Gộp Dashboard cũ thành 3 tab:
  1. Hồ sơ & Thống kê  (dữ liệu SQL)
  2. Sức khoẻ hệ thống  (CPU / RAM / Disk / Temp từ analytics_service)
  3. Thói quen & Gợi ý  (top apps + AI suggestions)
"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from view.ui_helpers import create_ui_footer
from view.widgets.base_dialog import FooterDialog

_DIALOG_STYLE = """
    QDialog {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                       stop:0 #0f0f1a, stop:1 #1a1a2a);
        color: white;
    }
    QLabel {
        color: white;
        font-size: 14px;
    }
    QLabel#title {
        color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                       stop:0 #00ffaa, stop:1 #00ccff);
        font-size: 22px;
        font-weight: bold;
        padding: 5px;
    }
    QTabWidget::pane {
        border: 1px solid rgba(0, 255, 136, 30);
        background: rgba(15, 15, 26, 200);
        border-radius: 8px;
    }
    QTabBar::tab {
        background: rgba(0, 0, 0, 100);
        color: rgba(255, 255, 255, 180);
        padding: 10px 20px;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        margin-right: 2px;
        font-weight: bold;
    }
    QTabBar::tab:selected {
        background: rgba(0, 255, 136, 20);
        color: #00ff88;
        border-bottom: 2px solid #00ff88;
    }
    QTabBar::tab:hover {
        background: rgba(0, 255, 136, 10);
        color: white;
    }
    QFrame#stat_card {
        background: rgba(0, 255, 136, 10);
        border: 1px solid rgba(0, 255, 136, 30);
        border-radius: 10px;
        padding: 10px;
    }
    QLabel#stat_value {
        color: #00ffaa;
        font-size: 22px;
        font-weight: bold;
    }
    QLabel#stat_label {
        color: rgba(255, 255, 255, 180);
        font-size: 12px;
    }
    QProgressBar {
        border: 1px solid rgba(0, 255, 136, 50);
        border-radius: 5px;
        background: rgba(25, 25, 45, 180);
        height: 15px;
        text-align: center;
        color: white;
    }
    QProgressBar::chunk {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                       stop:0 #00ff88, stop:1 #00ccff);
        border-radius: 5px;
    }
    QPushButton {
        background: rgba(0, 255, 136, 20);
        border: 1px solid rgba(0, 255, 136, 50);
        border-radius: 8px;
        padding: 8px 16px;
        color: #00ff88;
        font-size: 12px;
        font-weight: bold;
    }
    QPushButton:hover {
        background: rgba(0, 255, 136, 40);
    }
    QTextEdit {
        background: rgba(25, 25, 45, 180);
        border: 1px solid rgba(0, 255, 136, 40);
        border-radius: 10px;
        padding: 12px;
        color: white;
        font-size: 13px;
        font-family: 'Segoe UI';
    }
"""

_DETAILS_FRAME_STYLE = """
    QFrame {
        background: rgba(25, 25, 45, 100);
        border: 1px solid rgba(0, 255, 136, 20);
        border-radius: 8px;
        padding: 10px;
    }
    QLabel {
        font-size: 13px;
        color: #e0e0e0;
    }
"""

_HEALTH_FRAME_STYLE = """
    QFrame {
        background: rgba(25, 25, 45, 100);
        border: 1px solid rgba(0, 255, 136, 20);
        border-radius: 8px;
        padding: 15px;
    }
"""


class PersonalInfoDialog(FooterDialog):
    def __init__(self, user_name, sql_service, analytics_service=None, parent=None):
        super().__init__(parent)
        self.user_name = user_name
        self.sql_service = sql_service
        self.analytics_service = analytics_service
        self.setWindowTitle(" Thông tin cá nhân & Hiệu suất")
        self.setFixedSize(600, 680)
        self.setup_ui()
        self.load_data()
        create_ui_footer(self)

    # ------------------------------------------------------------------
    # UI Setup
    # ------------------------------------------------------------------

    def setup_ui(self):
        self.setStyleSheet(_DIALOG_STYLE)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Header title
        title = QLabel("Thông Tin Cá Nhân & Hiệu Suất")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Tab widget
        self.tabs = QTabWidget()
        self.tab_profile = QWidget()
        self.tab_health = QWidget()
        self.tab_habits = QWidget()

        self.setup_profile_tab()
        self.setup_health_tab()
        self.setup_habits_tab()

        self.tabs.addTab(self.tab_profile, "Hồ sơ & Thống kê")
        self.tabs.addTab(self.tab_health, "Sức khoẻ hệ thống")
        self.tabs.addTab(self.tab_habits, "Thói quen & Gợi ý")
        main_layout.addWidget(self.tabs)

        # Action buttons
        btn_layout = QHBoxLayout()
        self.refresh_btn = QPushButton("Làm mới dữ liệu")
        self.refresh_btn.clicked.connect(self.load_data)
        self.close_btn = QPushButton("Đóng")
        self.close_btn.clicked.connect(self.accept)
        btn_layout.addStretch()
        btn_layout.addWidget(self.refresh_btn)
        btn_layout.addWidget(self.close_btn)
        main_layout.addLayout(btn_layout)

    # ------------------------------------------------------------------
    # Tab: Profile & Stats
    # ------------------------------------------------------------------

    def setup_profile_tab(self):
        layout = QVBoxLayout(self.tab_profile)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)

        self.welcome_label = QLabel(f"Xin chào, {self.user_name}!")
        self.welcome_label.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #00ffaa;"
        )
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.welcome_label)

        grid = QGridLayout()
        grid.setSpacing(15)

        self.lbl_total_conversations = QLabel("0")
        self.lbl_total_conversations.setObjectName("stat_value")
        grid.addWidget(
            self._stat_card(self.lbl_total_conversations, "Tổng cuộc trò chuyện"), 0, 0
        )

        self.lbl_total_days = QLabel("0")
        self.lbl_total_days.setObjectName("stat_value")
        grid.addWidget(
            self._stat_card(self.lbl_total_days, "Số ngày hoạt động"), 0, 1
        )

        self.lbl_total_sessions = QLabel("0")
        self.lbl_total_sessions.setObjectName("stat_value")
        grid.addWidget(
            self._stat_card(self.lbl_total_sessions, "Số phiên kết nối"), 1, 0
        )

        self.lbl_avg_per_day = QLabel("0.0")
        self.lbl_avg_per_day.setObjectName("stat_value")
        grid.addWidget(
            self._stat_card(self.lbl_avg_per_day, "Trung bình / ngày"), 1, 1
        )

        layout.addLayout(grid)

        details_frame = QFrame()
        details_frame.setStyleSheet(_DETAILS_FRAME_STYLE)
        details_layout = QVBoxLayout(details_frame)
        self.lbl_current_session = QLabel("Phiên hiện tại: Chưa bắt đầu")
        self.lbl_start_date = QLabel("Ngày bắt đầu sử dụng: --")
        details_layout.addWidget(self.lbl_current_session)
        details_layout.addWidget(self.lbl_start_date)
        layout.addWidget(details_frame)
        layout.addStretch()

    # ------------------------------------------------------------------
    # Tab: System Health
    # ------------------------------------------------------------------

    def setup_health_tab(self):
        layout = QVBoxLayout(self.tab_health)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)

        stats_grid = QGridLayout()
        stats_grid.setSpacing(15)

        self.lbl_active_hours = QLabel("0.0")
        self.lbl_active_hours.setObjectName("stat_value")
        stats_grid.addWidget(
            self._stat_card(self.lbl_active_hours, "Giờ hoạt động (7 ngày)"), 0, 0
        )

        self.lbl_active_apps = QLabel("0")
        self.lbl_active_apps.setObjectName("stat_value")
        stats_grid.addWidget(
            self._stat_card(self.lbl_active_apps, "Tổng ứng dụng mở"), 0, 1
        )

        layout.addLayout(stats_grid)

        health_frame = QFrame()
        health_frame.setStyleSheet(_HEALTH_FRAME_STYLE)
        health_layout = QVBoxLayout(health_frame)
        health_layout.setSpacing(12)

        self.cpu_bar, self.cpu_value = self._metric_row(health_layout, "CPU trung bình:")
        self.ram_bar, self.ram_value = self._metric_row(health_layout, "RAM trung bình:")
        self.disk_bar, self.disk_value = self._metric_row(health_layout, "Disk trung bình:")

        # Temperature (no bar)
        temp_layout = QHBoxLayout()
        temp_layout.addWidget(QLabel("Nhiệt độ TB:"))
        temp_layout.addStretch()
        self.temp_value = QLabel("--°C")
        self.temp_value.setStyleSheet(
            "color: #00ffaa; font-weight: bold; font-size: 16px;"
        )
        temp_layout.addWidget(self.temp_value)
        health_layout.addLayout(temp_layout)

        layout.addWidget(health_frame)
        layout.addStretch()

    # ------------------------------------------------------------------
    # Tab: Habits & Suggestions
    # ------------------------------------------------------------------

    def setup_habits_tab(self):
        layout = QVBoxLayout(self.tab_habits)
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)

        layout.addWidget(QLabel("🔥 Top ứng dụng hay mở:"))
        self.txt_top_apps = QTextEdit()
        self.txt_top_apps.setReadOnly(True)
        self.txt_top_apps.setMaximumHeight(150)
        layout.addWidget(self.txt_top_apps)

        layout.addWidget(QLabel("💡 Gợi ý tối ưu hệ thống:"))
        self.txt_suggestions = QTextEdit()
        self.txt_suggestions.setReadOnly(True)
        self.txt_suggestions.setMaximumHeight(180)
        layout.addWidget(self.txt_suggestions)

    # ------------------------------------------------------------------
    # Data Loading
    # ------------------------------------------------------------------

    def load_data(self):
        """Tải dữ liệu từ sql_service và analytics_service."""
        self._load_sql_stats()
        self._load_analytics()

    def _load_sql_stats(self):
        """Load thống kê người dùng từ SQL."""
        if not self.sql_service:
            print("[PersonalInfoDialog] sql_service is None")
            return
        
        try:
            stats = self.sql_service.get_user_stats(self.user_name)
            if stats:
                self.lbl_total_conversations.setText(
                    str(stats.get('total_conversations', 0))
                )
                self.lbl_total_days.setText(str(stats.get('total_days', 0)))
                self.lbl_total_sessions.setText(str(stats.get('total_sessions', 0)))
                self.lbl_avg_per_day.setText(
                    f"{stats.get('avg_per_day', 0.0):.1f}"
                )

            cur_session = self.sql_service.current_session_id or 'Chưa bắt đầu'
            self.lbl_current_session.setText(f"Phiên hiện tại: {cur_session}")

            start_date = self.sql_service.get_first_use_date(self.user_name) or '--'
            self.lbl_start_date.setText(f"Ngày bắt đầu sử dụng: {start_date}")
        except Exception as e:
            print(f"[PersonalInfoDialog] Error loading user stats: {e}")

    def _load_analytics(self):
        """Load dữ liệu phân tích hệ thống từ analytics_service."""
        if not self.analytics_service:
            self.lbl_active_hours.setText("--")
            self.lbl_active_apps.setText("--")
            self.txt_top_apps.setPlainText("Không có dịch vụ phân tích hệ thống.")
            self.txt_suggestions.setPlainText("Không có dịch vụ phân tích hệ thống.")
            for lbl in (self.cpu_value, self.ram_value, self.disk_value):
                lbl.setText("--")
            self.temp_value.setText("--")
            return

        try:
            data = self.analytics_service.get_dashboard_data()
            report = data.get('weekly_report', {})

            self.lbl_active_hours.setText(f"{report.get('total_hours', 0.0):.1f}")

            total_apps = sum(
                item[1] for item in report.get('top_apps', []) if len(item) >= 2
            )
            self.lbl_active_apps.setText(str(total_apps))

            self._update_health_bars(report.get('health', {}))
            self._update_top_apps(report.get('top_apps', []))
            self._update_suggestions(report.get('suggestions', []))
        except Exception as e:
            print(f"[PersonalInfoDialog] Error loading analytics: {e}")

    def _update_health_bars(self, health: dict):
        if not health:
            self.temp_value.setText("--°C")
            return

        cpu = health.get('avg_cpu', 0)
        self.cpu_bar.setValue(int(cpu))
        self.cpu_value.setText(f"{cpu:.0f}%")

        ram = health.get('avg_ram', 0)
        self.ram_bar.setValue(int(ram))
        self.ram_value.setText(f"{ram:.0f}%")

        disk = health.get('avg_disk', 0)
        self.disk_bar.setValue(int(disk))
        self.disk_value.setText(f"{disk:.0f}%")

        avg_temp = health.get('avg_temp')
        self.temp_value.setText(
            f"{avg_temp:.1f}°C" if avg_temp and avg_temp > 0 else "--°C"
        )

    def _update_top_apps(self, top_apps: list):
        lines = []
        for i, item in enumerate(top_apps, 1):
            try:
                app = item[0]
                count = item[1]
                lines.append(f"{i}. {app}: {count} lần")
            except Exception:
                continue
        self.txt_top_apps.setPlainText(
            "\n".join(lines) if lines else "Chưa có dữ liệu ứng dụng"
        )

    def _update_suggestions(self, suggestions: list):
        if suggestions:
            text = "\n\n".join(f"{i}. {s}" for i, s in enumerate(suggestions, 1))
        else:
            text = "Máy của bạn đang hoạt động tốt! Không có gợi ý nào."
        self.txt_suggestions.setPlainText(text)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _stat_card(value_label: QLabel, sublabel_text: str) -> QFrame:
        """Tạo card thống kê gồm giá trị lớn + nhãn nhỏ."""
        card = QFrame()
        card.setObjectName("stat_card")
        layout = QVBoxLayout(card)
        layout.setSpacing(5)
        layout.setContentsMargins(10, 10, 10, 10)

        sub = QLabel(sublabel_text)
        sub.setObjectName("stat_label")

        layout.addWidget(value_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(sub, alignment=Qt.AlignmentFlag.AlignCenter)
        return card

    @staticmethod
    def _metric_row(parent_layout: QVBoxLayout, label_text: str):
        """Tạo một hàng metric gồm label + progress bar + giá trị %."""
        row = QHBoxLayout()
        lbl = QLabel(label_text)
        bar = QProgressBar()
        val = QLabel("0%")
        val.setStyleSheet("color: #00ffaa; font-weight: bold;")
        row.addWidget(lbl)
        row.addWidget(bar, 1)
        row.addWidget(val)
        parent_layout.addLayout(row)
        return bar, val
