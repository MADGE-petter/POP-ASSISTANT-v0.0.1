"""Dashboard Dialog - Analytics Dashboard matching Pop Assistant widget style"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class DashboardDialog(QDialog):
    """Dashboard hiển thị thống kê sử dụng và sức khỏe máy"""
    
    def __init__(self, analytics_service, parent=None):
        super().__init__(parent)
        self.analytics_service = analytics_service
        self.setWindowTitle(" Dashboard Analytics")
        self.setFixedSize(600, 700)
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """Setup UI với style matching Pop Assistant widgets"""
        self.setStyleSheet("""
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
                font-size: 24px;
                font-weight: bold;
                padding: 10px;
            }
            QLabel#section_title {
                color: #00ff88;
                font-size: 16px;
                font-weight: bold;
                padding-top: 15px;
                padding-bottom: 5px;
            }
            QLabel#stat_value {
                color: #00ffaa;
                font-size: 28px;
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
                padding: 15px;
                color: white;
                font-size: 13px;
                font-family: 'Segoe UI';
            }
            QFrame#stat_card {
                background: rgba(0, 255, 136, 10);
                border: 1px solid rgba(0, 255, 136, 30);
                border-radius: 10px;
                padding: 15px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel(" Dashboard Analytics")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Scroll area for content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
        """)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(15)
        
        # ===== THỐNG KÊ TỔNG QUAN =====
        stats_section = QLabel(" Thống kê tổng quan")
        stats_section.setObjectName("section_title")
        scroll_layout.addWidget(stats_section)
        
        # Stats grid
        stats_grid = QGridLayout()
        stats_grid.setSpacing(15)
        
        # Total hours
        self.total_hours_label = QLabel("0.0")
        self.total_hours_label.setObjectName("stat_value")
        self.total_hours_sublabel = QLabel("giờ / 7 ngày")
        self.total_hours_sublabel.setObjectName("stat_label")
        
        hours_card = self._create_stat_card(self.total_hours_label, self.total_hours_sublabel)
        stats_grid.addWidget(hours_card, 0, 0)
        
        # Sessions count
        self.sessions_label = QLabel("0")
        self.sessions_label.setObjectName("stat_value")
        self.sessions_sublabel = QLabel("phiên trò chuyện")
        self.sessions_sublabel.setObjectName("stat_label")
        
        sessions_card = self._create_stat_card(self.sessions_label, self.sessions_sublabel)
        stats_grid.addWidget(sessions_card, 0, 1)
        
        # Apps opened
        self.apps_label = QLabel("0")
        self.apps_label.setObjectName("stat_value")
        self.apps_sublabel = QLabel("ứng dụng mở")
        self.apps_sublabel.setObjectName("stat_label")
        
        apps_card = self._create_stat_card(self.apps_label, self.apps_sublabel)
        stats_grid.addWidget(apps_card, 0, 2)
        
        scroll_layout.addLayout(stats_grid)
        
        # ===== SỨC KHỎE MÁY =====
        health_section = QLabel(" Sức khỏe máy (7 ngày)")
        health_section.setObjectName("section_title")
        scroll_layout.addWidget(health_section)
        
        # Health metrics
        health_layout = QVBoxLayout()
        
        # CPU
        cpu_layout = QHBoxLayout()
        cpu_label = QLabel("CPU trung bình:")
        self.cpu_bar = QProgressBar()
        self.cpu_bar.setRange(0, 100)
        self.cpu_bar.setValue(0)
        self.cpu_value = QLabel("0%")
        self.cpu_value.setStyleSheet("color: #00ffaa; font-weight: bold;")
        cpu_layout.addWidget(cpu_label)
        cpu_layout.addWidget(self.cpu_bar, 1)
        cpu_layout.addWidget(self.cpu_value)
        health_layout.addLayout(cpu_layout)
        
        # RAM
        ram_layout = QHBoxLayout()
        ram_label = QLabel("RAM trung bình:")
        self.ram_bar = QProgressBar()
        self.ram_bar.setRange(0, 100)
        self.ram_bar.setValue(0)
        self.ram_value = QLabel("0%")
        self.ram_value.setStyleSheet("color: #00ffaa; font-weight: bold;")
        ram_layout.addWidget(ram_label)
        ram_layout.addWidget(self.ram_bar, 1)
        ram_layout.addWidget(self.ram_value)
        health_layout.addLayout(ram_layout)
        
        # Disk
        disk_layout = QHBoxLayout()
        disk_label = QLabel("Disk trung bình:")
        self.disk_bar = QProgressBar()
        self.disk_bar.setRange(0, 100)
        self.disk_bar.setValue(0)
        self.disk_value = QLabel("0%")
        self.disk_value.setStyleSheet("color: #00ffaa; font-weight: bold;")
        disk_layout.addWidget(disk_label)
        disk_layout.addWidget(self.disk_bar, 1)
        disk_layout.addWidget(self.disk_value)
        health_layout.addLayout(disk_layout)
        
        # Temperature
        temp_layout = QHBoxLayout()
        temp_label = QLabel("Nhiệt độ TB:")
        self.temp_value = QLabel("--°C")
        self.temp_value.setStyleSheet("color: #00ffaa; font-weight: bold; font-size: 16px;")
        temp_layout.addWidget(temp_label)
        temp_layout.addStretch()
        temp_layout.addWidget(self.temp_value)
        health_layout.addLayout(temp_layout)
        
        scroll_layout.addLayout(health_layout)
        
        # ===== TOP ỨNG DỤNG =====
        apps_section = QLabel(" Top ứng dụng hay mở")
        apps_section.setObjectName("section_title")
        scroll_layout.addWidget(apps_section)
        
        self.apps_text = QTextEdit()
        self.apps_text.setReadOnly(True)
        self.apps_text.setMaximumHeight(150)
        scroll_layout.addWidget(self.apps_text)
        
        # ===== GỢI Ý TỐI ƯU =====
        suggestions_section = QLabel("💡 Gợi ý tối ưu")
        suggestions_section.setObjectName("section_title")
        scroll_layout.addWidget(suggestions_section)
        
        self.suggestions_text = QTextEdit()
        self.suggestions_text.setReadOnly(True)
        self.suggestions_text.setMaximumHeight(150)
        scroll_layout.addWidget(self.suggestions_text)
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        # Refresh button
        refresh_btn = QPushButton(" Làm mới dữ liệu")
        refresh_btn.clicked.connect(self.load_data)
        layout.addWidget(refresh_btn)
        
        # Close button
        close_btn = QPushButton(" Đóng")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
    
    def _create_stat_card(self, value_label, sublabel) -> QFrame:
        """Tạo stat card với style"""
        card = QFrame()
        card.setObjectName("stat_card")
        layout = QVBoxLayout(card)
        layout.setSpacing(5)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.addWidget(value_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(sublabel, alignment=Qt.AlignmentFlag.AlignCenter)
        return card
    
    def load_data(self):
        """Load dữ liệu từ analytics service"""
        try:
            data = self.analytics_service.get_dashboard_data()
            report = data['weekly_report']
            
            # Update stats
            self.total_hours_label.setText(f"{report['total_hours']:.1f}")
            self.sessions_label.setText(str(report['total_sessions']))
            
            # Handle both 2-value and 3-value tuples
            total_apps = 0
            for item in report['top_apps']:
                if len(item) >= 2:
                    total_apps += item[1]  # count is second element
            self.apps_label.setText(str(total_apps))
            
            # Update health bars
            health = report['health']
            if health:
                self.cpu_bar.setValue(int(health.get('avg_cpu', 0)))
                self.cpu_value.setText(f"{health.get('avg_cpu', 0):.0f}%")
                
                self.ram_bar.setValue(int(health.get('avg_ram', 0)))
                self.ram_value.setText(f"{health.get('avg_ram', 0):.0f}%")
                
                self.disk_bar.setValue(int(health.get('avg_disk', 0)))
                self.disk_value.setText(f"{health.get('avg_disk', 0):.0f}%")
                
                avg_temp = health.get('avg_temp')
                if avg_temp and avg_temp > 0:
                    self.temp_value.setText(f"{avg_temp:.1f}°C")
                else:
                    self.temp_value.setText("--°C")
            else:
                self.temp_value.setText("--°C")
            
            # Update top apps
            apps_text = ""
            for i, item in enumerate(report['top_apps'], 1):
                try:
                    # Handle both 2-value (app, count) and 3-value (app, count, timestamp) tuples
                    if len(item) == 2:
                        app, count = item
                    elif len(item) >= 3:
                        app, count = item[0], item[1]  # ignore timestamp
                    else:
                        continue
                    apps_text += f"{i}. {app}: {count} lần\n"
                except Exception:
                    continue
            if not apps_text:
                apps_text = "Chưa có dữ liệu ứng dụng"
            self.apps_text.setPlainText(apps_text)
            
            # Update suggestions
            suggestions_text = ""
            if report['suggestions']:
                for i, suggestion in enumerate(report['suggestions'], 1):
                    suggestions_text += f"{i}. {suggestion}\n\n"
            else:
                suggestions_text = "Máy của bạn đang hoạt động tốt! Không có gợi ý nào."
            self.suggestions_text.setPlainText(suggestions_text)
            
        except Exception as e:
            print(f"[DashboardDialog] Error loading data: {e}")

