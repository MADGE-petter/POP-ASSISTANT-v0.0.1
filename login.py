#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pop Assistant - Login Launcher
Chạy giao diện đăng nhập
"""

import os
import sys

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication


def main():
    """Main function to run login application"""
    try:
        app = QApplication(sys.argv)
        app.setApplicationName("Pop Assistant Login")
        app.setOrganizationName("Pop AI")
        app.setQuitOnLastWindowClosed(True)
        
        # Set application icon
        try:
            from PyQt6.QtGui import QIcon
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'icon.png')
            if os.path.exists(icon_path):
                app.setWindowIcon(QIcon(icon_path))
            else:
                print(f"[Login] Icon not found: {icon_path}")
        except Exception as e:
            print(f"[Login] Could not set icon: {e}")

        # Import temperature_monitor để quản lý OHM lifecycle
        _monitor_ref = None
        try:
            from model.temperature_monitor import _monitor
            _monitor_ref = _monitor
        except Exception as e:
            print(f"[Login] Không import được temperature_monitor: {e}")
        
        def on_app_exit():
            try:
                if _monitor_ref:
                    _monitor_ref.stop_ohm()
            except Exception as e:
                print(f"[Login] Lỗi dừng OHM: {e}")
        
        app.aboutToQuit.connect(on_app_exit)

        from service.login_service import LoginService
        from view.login_view import LoginView

        # Tạo Service ở Controller level (login.py đóng vai trò Controller)
        login_service = LoginService()
        
        class LoginWindowWithAdmin(LoginView):
            def __init__(self, admin_callback, login_service):
                super().__init__(login_service)
                self.admin_callback = admin_callback
                self.alt_count = 0
                
                self.key_timer = QTimer()
                self.key_timer.timeout.connect(self.clear_keys)
                self.key_timer.setSingleShot(True)
            
            def keyPressEvent(self, event):
                key = event.key()
                # Detect Alt key
                if key == Qt.Key.Key_Alt:
                    self.alt_count += 1
                    if self.alt_count >= 3:
                        self.admin_callback() 
                        self.alt_count = 0
                    else:
                        self.key_timer.start(2000)
                
                super().keyPressEvent(event)   
            def clear_keys(self):
                self.alt_count = 0

        global admin_login_ref, admin_panel_ref
        admin_login_ref = None
        admin_panel_ref = None
        
        def open_admin_login():
            global admin_login_ref
            try:
                from admin.view.admin_login import AdminLoginView
                admin_login = AdminLoginView()
                admin_login.login_success.connect(on_admin_login_success)
                admin_login.show()
                admin_login.raise_()
                admin_login.activateWindow()
                app.processEvents()
                QTimer.singleShot(100, lambda: None)
                app.processEvents()
                login_window.hide()
                admin_login_ref = admin_login
                
                # Debug: Check widgets immediately
                widgets = QApplication.topLevelWidgets()
                print(f"Widgets immediately after admin login: {len(widgets)}")
                for i, w in enumerate(widgets):
                    is_visible = w.isVisible()
                    title = w.windowTitle() if hasattr(w, 'windowTitle') else 'No Title'
                    w_type = type(w).__name__
                    print(f"  Widget {i}: {title} - {w_type} - Visible: {is_visible}")
                
            except ImportError as e:
                print(f"Lỗi import admin_login: {e}")
                import traceback
                traceback.print_exc()
            except Exception as e:
                print(f"Lỗi mở admin login: {e}")
                import traceback
                traceback.print_exc()
        
        def on_admin_login_success(username):
            """Handle admin login success"""
            global admin_panel_ref
            try:
                print(f"Admin login successful for: {username}")
                from admin.view.admin_panel import create_admin_panel
                admin_panel = create_admin_panel()
                
                # Lưu reference để không bị garbage collected
                admin_panel_ref = admin_panel
                
                # Force show admin panel
                admin_panel.show()
                admin_panel.raise_()
                admin_panel.activateWindow()
                admin_panel.setFocus()
                
                # Force process events để admin panel thực sự hiển thị
                app.processEvents()
                QTimer.singleShot(100, lambda: None)
                app.processEvents()
                
                # Đóng admin login window
                if 'admin_login_ref' in globals() and admin_login_ref:
                    admin_login_ref.close()
                def on_admin_panel_close():
                    print("Admin panel closed, returning to login...")
                    # Không gọi main() lại, chỉ đóng admin panel
                
                admin_panel.closeEvent = lambda e: (on_admin_panel_close(), e.accept())
                
            except ImportError as e:
                print(f"Lỗi import admin_panel: {e}")
                import traceback
                traceback.print_exc()
            except Exception as e:
                print(f"Lỗi mở admin panel: {e}")
                import traceback
                traceback.print_exc()

        login_window = None
        main_window = None
        
        def on_login_success(username):
            nonlocal main_window
            print(f"Login successful: {username}")
            
            try:
                # Import and run main application
                import main
                main_window = main.create_main_window(username)
                
                if main_window is None:
                    return
                
                # Show main window with force methods
                main_window.show()
                main_window.raise_()
                main_window.activateWindow()
                main_window.setFocus()
                
                # Close login immediately
                login_window.close()              
            except ImportError as e:
                print(f"Lỗi import: {e}")
                import traceback
                traceback.print_exc()
                login_window.show()
            except Exception as e:
                print(f"Lỗi khởi tạo giao diện chính: {e}")
                import traceback
                traceback.print_exc()
                login_window.show()
        
        # Bây giờ mới tạo login window với admin callback
         # Controller inject Service vào View
        login_window = LoginWindowWithAdmin(open_admin_login, login_service)
        login_window.login_success.connect(on_login_success)
        
        # Show login window
        login_window.show()    
        # Run the application
        result = app.exec()
        # Check final state
        widgets = QApplication.topLevelWidgets()
        visible_count = 0
        for widget in widgets:
            if widget.isVisible():
                visible_count += 1
                title = widget.windowTitle() if hasattr(widget, 'windowTitle') else 'No Title'
                print(f"  Visible: {title}")
        
        print(f"Total visible: {visible_count}")
            
    except ImportError as e:
        print(f"Chi tiết lỗi: {e}")
        input("Nhấn Enter để thoát...")
    except Exception as e:
        print(f"Lỗi khởi động ứng dụng: {e}")
        input("Nhấn Enter để thoát...")

if __name__ == "__main__":
    main()
