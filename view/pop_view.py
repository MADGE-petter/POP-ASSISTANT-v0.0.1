import os
import sys
import time

from PyQt6.QtCore import QPoint, Qt, QThread, QTimer, pyqtSignal
from PyQt6.QtGui import (
    QAction,
    QBrush,
    QColor,
    QFont,
    QIcon,
    QPainter,
    QPen,
    QRadialGradient,
)
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMenu,
    QMenuBar,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSlider,
    QSpinBox,
    QSystemTrayIcon,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from view.ui_helpers import create_ui_footer, position_ui_footer
from view.widgets import (
    AudioDialog,
    HistoryUsageDialog,
    HistoryWindow,
    PersonalInfoDialog,
    SettingsDialog,
)


class SoundWaveWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.animation_offset = 0
        self.setMinimumHeight(180)
        self.setMinimumWidth(300)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw sound waves with better design
        center_x = self.width() // 2
        center_y = self.height() // 2
        
        # Draw multiple circles with gradient effect
        for i in range(4):
            radius = 20 + (i * 20) + (self.animation_offset % 15)
            alpha = max(0.1, 0.7 - (i * 0.15))
            
            # Create gradient for each circle
            gradient = QRadialGradient(center_x, center_y, radius)
            gradient.setColorAt(0, QColor(0, 255, 136, int(alpha * 255)))
            gradient.setColorAt(0.7, QColor(0, 200, 120, int(alpha * 200)))
            gradient.setColorAt(1, QColor(0, 150, 100, int(alpha * 100)))
            
            painter.setPen(QPen(QColor(0, 255, 136, int(alpha * 255)), 2))
            painter.setBrush(QBrush(gradient))
            
            painter.drawEllipse(center_x - radius, center_y - radius, 
                              radius * 2, radius * 2)
        
        # Central orb
        orb_gradient = QRadialGradient(center_x, center_y, 25)
        orb_gradient.setColorAt(0, QColor(150, 255, 200))
        orb_gradient.setColorAt(0.5, QColor(0, 255, 136))
        orb_gradient.setColorAt(1, QColor(0, 200, 100))
        
        painter.setPen(QPen(QColor(0, 255, 136, 150), 2))
        painter.setBrush(QBrush(orb_gradient))
        painter.drawEllipse(center_x - 25, center_y - 25, 50, 50)
        
        painter.end()
    
    def update_animation(self):
        self.animation_offset += 1
        self.update()

class PopView(QMainWindow):
    """View layer - Chỉ quản lý UI, không business logic."""
    
    updateUserTextSignal = pyqtSignal(str)
    updateBotTextSignal = pyqtSignal(str)
    
    def __init__(self, controller=None):
        super().__init__()
        
        # Controller injects services - View chỉ giữ controller reference
        self.controller = controller
        
        self.setWindowTitle("Pop Assistant")
        self.setGeometry(100, 100, 450, 650)
        
        # Set application icon
        try:
            from PyQt6.QtGui import QPixmap

            from utils.paths import resource_path

            png_path = resource_path("assets", "icon.png")
            if os.path.exists(png_path):
                pixmap = QPixmap(png_path)
                icon = QIcon(png_path)
                if not icon.isNull() and pixmap.width() > 0:
                    self.setWindowIcon(icon)
            else:
                ico_path = resource_path("assets", "icon.ico")
                if os.path.exists(ico_path):
                    self.setWindowIcon(QIcon(ico_path))
        except Exception:
            pass
        
        # Assistant properties - từ controller
        self.assistant_active = False
        self.assistant_started = False
        self.user_name = "bạn"
        self.assistant_name = "Pop"
        
        # Không tạo services ở đây - chỉ nhận controller
        # Tất cả service access qua controller
        self.controller = None
        
        # Settings
        self.settings = {
            'auto_start': True,
            'voice_enabled': True,
            'theme': 'dark'
        }
        
        # History viewer widget
        self.history_widget = None
        
        # Setup UI
        self.setup_ui()
        
        # Setup animation
        self.setup_animation()
        
        # Sleep mode
        self.is_sleeping = False
        self.sleep_timer = QTimer(self)
        self.sleep_timer.timeout.connect(self._enter_sleep_mode)
        self.sleep_timeout = 30000  # 30 giây không hoạt động -> sleep
        self.last_activity_time = time.time()

        # Thread-safe text updates
        self.updateUserTextSignal.connect(self._on_update_user_text)
        self.updateBotTextSignal.connect(self._on_update_bot_text)
        
        # System Tray
        self.tray_icon = None
        self.startup_mode = '--startup' in sys.argv  # Check if launched at startup
        
    def _enter_sleep_mode(self):
        """Thu nhỏ cửa sổ và chuyển sang trạng thái ngủ"""
        if self.is_sleeping:
            return
        
        print("[PopView] Entering sleep mode...")
        self.is_sleeping = True
        
        # Thu nhỏ cửa sổ
        self.showMinimized()
        
        # Thông báo cho Controller
        if self.controller and hasattr(self.controller, 'on_sleep_mode_entered'):
            self.controller.on_sleep_mode_entered()
        
    def set_controller(self, controller):
        """Kết nối với controller - View nhận services từ Controller, không tự tạo"""
        self.controller = controller
        
        # Tạo menu bar
        self.create_menu()
    
    
    def show_settings_dialog(self):
        """Hiển thị dialog cài đặt hệ thống"""
        dialog = SettingsDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            settings = dialog.get_settings()
            QMessageBox.information(self, "Thành công", "Đã lưu cài đặt!")
            # Apply settings if needed
            self.settings.update(settings)
    
    def show_audio_dialog(self):
        """Hiển thị dialog cài đặt âm thanh"""
        dialog = AudioDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            audio_settings = dialog.get_audio_settings()
            QMessageBox.information(self, "Thành công", "Đã lưu cài đặt âm thanh!")
            # Apply audio settings if needed
    
    def logout(self):
        """Đăng xuất người dùng hiện tại"""
        reply = QMessageBox.question(
            self, "Xác nhận", "Bạn có chắc muốn đăng xuất?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            QMessageBox.information(self, "Thành công", "Đã đăng xuất thành công!")
            self.close()
    
    def show_history_dialog(self):
        """Hiển thị dialog lịch sử sử dụng"""
        dialog = HistoryUsageDialog(self)
        dialog.exec()
    
    def show_alert_notification(self, alert_data):
        """Hiển thị thông báo cảnh báo với thông tin chi tiết"""
        # Ensure UI updates happen on the main thread
        if self.thread() != QThread.currentThread():
            QTimer.singleShot(0, lambda: self.show_alert_notification(alert_data))
            return
        try:
            from PyQt6.QtCore import Qt
            from PyQt6.QtWidgets import QMessageBox

            # Xác định icon dựa trên level
            level = alert_data.get('level', 'warning').lower()
            if level == 'critical':
                icon = QMessageBox.Icon.Critical
                title = "CẢNH BÁO NGUY HIỂM!"
            elif level == 'danger':
                icon = QMessageBox.Icon.Warning
                title = "CẢNH BÁO NGUY HIỂM!"
            else:
                icon = QMessageBox.Icon.Warning
                title = "Cảnh báo hệ thống"
            
            # Tạo message box
            msg_box = QMessageBox(self)
            msg_box.setIcon(icon)
            msg_box.setWindowTitle(title)
            msg_box.setText(alert_data.get('message', 'Có cảnh báo hệ thống'))
            
            # Thêm thông tin chi tiết nếu có
            detailed_text = []
            if 'value' in alert_data:
                detailed_text.append(f"Giá trị hiện tại: {alert_data['value']}")
            if 'metric' in alert_data:
                detailed_text.append(f"Loại: {alert_data['metric'].upper()}")
            if 'timestamp' in alert_data:
                detailed_text.append(f"Thời gian: {alert_data['timestamp']}")
            
            if detailed_text:
                msg_box.setDetailedText("\n".join(detailed_text))
            
            # Thêm buttons
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.setModal(True)
            msg_box.open()
            
        except Exception as e:
            print(f"[PopView] Error showing alert notification: {e}")
            try:
                QMessageBox.warning(self, "Cảnh báo", str(alert_data.get('message', 'Có cảnh báo hệ thống')))
            except Exception:
                pass
    
    def setup_ui(self):
        """Create all UI elements"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Set elegant dark background with subtle gradient
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                               stop:0 #0f0f1a, stop:1 #1a1a2a);
            }
        """)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)
        
        # Pop Assistant title with larger font
        title_label = QLabel("Pop Assistant")
        title_label.setStyleSheet("""
            QLabel {
                color: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                               stop:0 #00ffaa, stop:1 #00ccff);
                font-size: 32px;
                font-weight: bold;
                text-align: center;
                padding: 15px;
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Enhanced sound wave widget with subtle border
        self.sound_wave_widget = SoundWaveWidget()
        self.sound_wave_widget.setStyleSheet("""
            SoundWaveWidget {
                background: rgba(0, 20, 40, 30);
                border: 1px solid rgba(0, 255, 136, 20);
                border-radius: 15px;
            }
        """)
        main_layout.addWidget(self.sound_wave_widget)
        
        # Elegant conversation display
        self.user_text_label = QLabel("")
        self.user_text_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 220);
                background: rgba(255, 255, 255, 5);
                border: 1px solid rgba(255, 255, 255, 10);
                border-radius: 10px;
                font-size: 16px;
                font-family: 'Segoe UI';
                padding: 15px;
                text-align: center;
            }
        """)
        self.user_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.user_text_label.setWordWrap(True)
        main_layout.addWidget(self.user_text_label)
        
        self.bot_text_label = QLabel("Sẵn sàng...")
        self.bot_text_label.setStyleSheet("""
            QLabel {
                color: rgba(0, 255, 200, 220);
                background: rgba(0, 255, 136, 5);
                border: 1px solid rgba(0, 255, 136, 20);
                border-radius: 10px;
                font-size: 16px;
                font-family: 'Segoe UI';
                padding: 15px;
                text-align: center;
            }
        """)
        self.bot_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bot_text_label.setWordWrap(True)
        main_layout.addWidget(self.bot_text_label)
        
        # Add stretch for centering
        main_layout.addStretch()
        
        # Add menu button in corner
        self.menu_btn = QPushButton("⋮")
        self.menu_btn.setFixedSize(35, 35)
        self.menu_btn.setStyleSheet("""
            QPushButton {
                background: rgba(0, 255, 136, 10);
                border: 1px solid rgba(0, 255, 136, 25);
                border-radius: 17px;
                color: #00ff88;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(0, 255, 136, 25);
                border: 1px solid rgba(0, 255, 136, 50);
            }
            QPushButton:pressed {
                background: rgba(0, 255, 136, 35);
            }
        """)
        self.menu_btn.clicked.connect(self.show_menu)
        
        # Position button in top-right corner
        self.menu_btn.setParent(central_widget)
        self.update_menu_button_position()
        
        # Create menu
        self.create_menu()
        create_ui_footer(self)
    
    def setup_animation(self):
        """Setup animation timer"""
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.start(50)  # 20 FPS
    
    def update_animation(self):
        """Update the sound wave animation"""
        if hasattr(self, 'sound_wave_widget'):
            self.sound_wave_widget.update_animation()
    
    def speak_ui(self, text):
        """UI wrapper for speak function - delegated to controller."""
        if self.controller:
            self.controller.speak(text)
    
    def get_voice_ui(self):
        """UI wrapper for get_voice function - delegated to controller."""
        if self.controller:
            return self.controller.listen()
        return None
    
    def get_text_ui(self):
        """Get text with retry logic - delegated to controller."""
        if self.controller:
            return self.controller.listen()
        return None
    
    def update_user_text(self, text):
        """Update user text label."""
        if hasattr(self, 'user_text_label'):
            self.updateUserTextSignal.emit(text)
    
    def update_bot_text(self, text):
        """Update bot text label."""
        if hasattr(self, 'bot_text_label'):
            self.updateBotTextSignal.emit(text)

    def _on_update_user_text(self, text):
        if hasattr(self, 'user_text_label'):
            self.user_text_label.setText(text)

    def _on_update_bot_text(self, text):
        if hasattr(self, 'bot_text_label'):
            self.bot_text_label.setText(text)
    
    def create_menu(self):
        """Tạo menu với 3 lựa chọn"""
        self.menu = QMenu(self)
        self.menu.setStyleSheet("""
            QMenu {
                background: rgba(20, 20, 35, 200);
                border: 1px solid rgba(0, 255, 136, 40);
                border-radius: 8px;
                padding: 5px;
            }
            QMenu::item {
                background: transparent;
                color: #00ffaa;
                padding: 8px 20px;
                border-radius: 4px;
                font-size: 14px;
                font-weight: 600;
            }
            QMenu::item:selected {
                background: rgba(0, 255, 136, 30);
                color: #ffffff;
            }
            QMenu::separator {
                height: 1px;
                background: rgba(0, 255, 136, 20);
                margin: 5px 10px;
            }
        """)
        
        # Thêm các hành động (không icon)
        personal_action = QAction("Cá nhân", self)
        personal_action.triggered.connect(self.show_personal_info)
        self.menu.addAction(personal_action)
        
        settings_action = QAction("Cài đặt", self)
        settings_action.triggered.connect(self.show_settings_dialog)
        self.menu.addAction(settings_action)
        
        audio_action = QAction("Âm thanh", self)
        audio_action.triggered.connect(self.show_audio_dialog)
        self.menu.addAction(audio_action)
        
        history_action = QAction("Lịch sử trò chuyện", self)
        history_action.triggered.connect(self.show_history)
        self.menu.addAction(history_action)
        
        self.menu.addSeparator()
        
        signout_action = QAction("Sign out", self)
        signout_action.triggered.connect(self.sign_out)
        self.menu.addAction(signout_action)
        
        self.menu.addSeparator()
        
        # Quit action
        quit_action = QAction("Thoát", self)
        quit_action.triggered.connect(self._quit_app)
        self.menu.addAction(quit_action)
    
    def _quit_app(self):
        """Thoát hoàn toàn ứng dụng"""
        print("[PopView] Quitting application...")
        
        # Stop via controller
        if self.controller:
            self.controller.stop()
        
        # Hide tray icon
        if self.tray_icon:
            self.tray_icon.hide()
        
        # Quit application
        QApplication.quit()
    
    def keyPressEvent(self, event):
        """Xử lý phím tắt"""
        # ESC: Minimize to tray (hoặc quit nếu đang giữ Shift)
        if event.key() == Qt.Key.Key_Escape:
            if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                # Shift+ESC: Quit completely
                self._quit_app()
            else:
                # ESC: Minimize to sleep mode
                self._enter_sleep_mode()
        else:
            super().keyPressEvent(event)
    
    def show_menu(self):
        """Hiển thị menu tại vị trí nút"""
        if hasattr(self, 'menu_btn') and hasattr(self, 'menu'):
            # Lấy vị trí của nút
            btn_pos = self.menu_btn.mapToGlobal(QPoint(0, 0))
            # Hiển thị menu bên dưới nút
            menu_x = btn_pos.x() + self.menu_btn.width() - self.menu.sizeHint().width()
            menu_y = btn_pos.y() + self.menu_btn.height() + 5
            self.menu.exec(QPoint(menu_x, menu_y))
    
    def update_menu_button_position(self):
        """Cập nhật vị trí nút menu ở góc trên bên phải"""
        if hasattr(self, 'menu_btn'):
            self.menu_btn.move(self.width() - 45, 15)
    
    def show_settings_dialog(self):
        """Hiển thị dialog cài đặt hệ thống"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Cài đặt")
        dialog.setFixedSize(450, 400)
        dialog.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                               stop:0 #1a1f2a, stop:1 #2a2f3a);
                color: #e0e0e0;
            }
            QLabel {
                color: #e0e0e0;
                font-size: 12px;
                padding: 5px;
            }
            QCheckBox {
                color: #e0e0e0;
                font-size: 12px;
                padding: 5px;
            }
            QSpinBox {
                background: rgba(30, 35, 50, 90);
                border: 1px solid rgba(0, 255, 170, 40);
                border-radius: 6px;
                padding: 8px;
                color: #e0e0e0;
                font-size: 12px;
            }
            QSlider {
                min-height: 20px;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                               stop:0 rgba(39, 174, 96, 0.8), stop:1 rgba(34, 153, 84, 0.8));
                border: 2px solid rgba(39, 174, 96, 0.9);
                border-radius: 8px;
                color: #ffffff;
                font-size: 12px;
                font-weight: 700;
                padding: 8px 16px;
            }
        """)
        
        layout = QVBoxLayout(dialog)
        
        # Auto start assistant
        auto_start_cb = QCheckBox(" Tự động khởi động assistant")
        auto_start_cb.setChecked(True)
        
        # Assistant delay
        delay_layout = QHBoxLayout()
        delay_label = QLabel("⏱ Thời gian trễ (ms):")
        delay_spin = QSpinBox()
        delay_spin.setRange(100, 5000)
        delay_spin.setValue(1000)
        delay_layout.addWidget(delay_label)
        delay_layout.addWidget(delay_spin)
        delay_layout.addStretch()
        
        # Speech recognition
        speech_cb = QCheckBox(" Nhận dạng giọng nói")
        speech_cb.setChecked(True)
        
        # Text to speech
        tts_cb = QCheckBox(" Đọc văn bản thành giọng nói")
        tts_cb.setChecked(True)
        
        # Volume
        volume_layout = QHBoxLayout()
        volume_label = QLabel(" Âm lượng:")
        volume_slider = QSlider(Qt.Orientation.Horizontal)
        volume_slider.setRange(0, 100)
        volume_slider.setValue(80)
        volume_layout.addWidget(volume_label)
        volume_layout.addWidget(volume_slider)
        volume_layout.addStretch()
        
        # Speech rate
        rate_layout = QHBoxLayout()
        rate_label = QLabel(" Tốc độ nói:")
        rate_spin = QSpinBox()
        rate_spin.setRange(50, 200)
        rate_spin.setValue(100)
        rate_layout.addWidget(rate_label)
        rate_layout.addWidget(rate_spin)
        rate_layout.addStretch()
        
        # Add widgets to layout
        layout.addWidget(auto_start_cb)
        layout.addLayout(delay_layout)
        layout.addWidget(speech_cb)
        layout.addWidget(tts_cb)
        layout.addLayout(volume_layout)
        layout.addLayout(rate_layout)
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton(" Lưu")
        cancel_btn = QPushButton(" Hủy")
        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        # Handle buttons
        def save_settings():
            QMessageBox.information(dialog, "Thành công", "Đã lưu cài đặt!")
            dialog.accept()
        
        save_btn.clicked.connect(save_settings)
        cancel_btn.clicked.connect(dialog.reject)
        
        dialog.exec()
    
    def show_audio_dialog(self):
        """Hiển thị dialog cài đặt âm thanh"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Âm thanh")
        dialog.setFixedSize(400, 300)
        dialog.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                               stop:0 #1a1f2a, stop:1 #2a2f3a);
                color: #e0e0e0;
            }
            QLabel {
                color: #e0e0e0;
                font-size: 12px;
                padding: 5px;
            }
            QSlider {
                min-height: 20px;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                               stop:0 rgba(243, 156, 18, 0.8), stop:1 rgba(230, 126, 34, 0.8));
                border: 2px solid rgba(243, 156, 18, 0.9);
                border-radius: 8px;
                color: #ffffff;
                font-size: 12px;
                font-weight: 700;
                padding: 8px 16px;
            }
        """)
        
        layout = QVBoxLayout(dialog)
        
        # Volume
        volume_layout = QHBoxLayout()
        volume_label = QLabel(" Âm lượng chính:")
        volume_slider = QSlider(Qt.Orientation.Horizontal)
        volume_slider.setRange(0, 100)
        volume_slider.setValue(80)
        volume_layout.addWidget(volume_label)
        volume_layout.addWidget(volume_slider)
        volume_layout.addStretch()
        
        # Speech rate
        rate_layout = QHBoxLayout()
        rate_label = QLabel(" Tốc độ nói:")
        rate_spin = QSpinBox()
        rate_spin.setRange(50, 200)
        rate_spin.setValue(100)
        rate_layout.addWidget(rate_label)
        rate_layout.addWidget(rate_spin)
        rate_layout.addStretch()
        
        # Add widgets
        layout.addLayout(volume_layout)
        layout.addLayout(rate_layout)
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton(" Lưu")
        cancel_btn = QPushButton(" Hủy")
        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        # Handle buttons
        def save_audio():
            QMessageBox.information(dialog, "Thành công", "Đã lưu cài đặt âm thanh!")
            dialog.accept()
        
        save_btn.clicked.connect(save_audio)
        cancel_btn.clicked.connect(dialog.reject)
        
        dialog.exec()
    
    def show_personal_info(self):
        """Hiển thị thông tin cá nhân"""
        sql = self.controller.sql if self.controller else None
        analytics = None
        if self.controller and hasattr(self.controller, 'system'):
            analytics = self.controller.system.analytics_service
        dialog = PersonalInfoDialog(self.user_name, sql, analytics, self)
        dialog.exec()
    
    def sign_out(self):
        """Đăng xuất và đóng ứng dụng"""
        from PyQt6.QtWidgets import QMessageBox
        
        reply = QMessageBox.question(
            self, 
            'Xác nhận đăng xuất',
            'Bạn có chắc chắn muốn đăng xuất?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Kết thúc phiên hiện tại - delegate to controller
            if self.controller:
                self.controller.stop()
            
            self.close()  # Đóng ứng dụng
    
    def resizeEvent(self, event):
        """Xử lý khi cửa sổ thay đổi kích thước"""
        super().resizeEvent(event)
        self.update_menu_button_position()
        position_ui_footer(self)
    
    def closeEvent(self, event):
        self.assistant_active = False
        
        # Đảm bảo assistant thread dừng hoàn toàn
        if hasattr(self, 'assistant_thread'):
            self.assistant_thread.join(timeout=2)
        
        if hasattr(self, 'animation_timer'):
            self.animation_timer.stop()
        
        # Database không cần close vì không có connection mở
        super().closeEvent(event)
    
    def show_history(self):
        """Hiển thị cửa sổ lịch sử trò chuyện"""
        if self.history_widget is None:
            # Get sql_service from controller
            sql = self.controller.sql if self.controller else None
            self.history_widget = HistoryWindow(sql, self.user_name)
            print("HistoryWindow created")
        self.history_widget.show()
        self.history_widget.raise_()
        self.history_widget.activateWindow()
        print("HistoryWindow shown from PopView")
    

    
    def add_message(self, text, is_user=False):
        """Thêm tin nhắn vào chat"""
        # Giả lập - cần điều chỉnh theo implementation thực tế của PopView
        prefix = "Bạn: " if is_user else "Bot: "
        print(f"[Chat] {prefix}{text}")


if __name__ == "__main__":
    pass
