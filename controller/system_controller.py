"""System Controller - Quản lý system monitoring, alerts, analytics."""

from typing import Optional

from controller.interfaces import IAlertManager, IAnalyticsService


class SystemController: 
    def __init__(self, 
                 alert_manager: Optional[IAlertManager] = None, 
                 analytics_service: Optional[IAnalyticsService] = None):
        self.alert_manager = alert_manager
        self.analytics_service = analytics_service
        
        # Temperature monitor reference
        self._monitor_ref = None
    
    def init_monitor(self, monitor_ref):
        """Inject temperature monitor reference."""
        self._monitor_ref = monitor_ref
    
    def start_monitoring(self, user_name="bạn"):
        """Bắt đầu giám sát hệ thống."""
        # Start alert manager
        if self.alert_manager:
            self.alert_manager.start()
        
        # Start analytics
        if self.analytics_service:
            self.analytics_service.start()
    
    def stop_monitoring(self):
        """Dừng giám sát hệ thống."""
        if self.alert_manager:
            self.alert_manager.stop()
        
        if self.analytics_service:
            self.analytics_service.stop()
        
        # Stop temperature monitor
        if self._monitor_ref:
            try:
                self._monitor_ref.stop_ohm()
            except Exception:
                pass
    
    def set_sleep_mode(self, enabled):
        """Thiết lập chế độ ngủ cho các services."""
        if self.alert_manager:
            self.alert_manager.set_sleep_mode(enabled)
    
    def reset_wellness_timers(self):
        """Reset wellness timers khi user tương tác."""
        if self.alert_manager:
            self.alert_manager.reset_wellness_timers()
    
    def get_system_status(self):
        """Lấy trạng thái hệ thống."""
        if self.alert_manager:
            return self.alert_manager.get_system_status()
        return {}
    
    def on_alert_triggered(self, alert_data):
        """Callback khi có cảnh báo."""
        # Sẽ được gán từ bên ngoài để hiển thị UI
        pass
    
    def get_analytics_summary(self):
        """Lấy tóm tắt analytics."""
        if self.analytics_service:
            return self.analytics_service.get_summary()
        return {}
    
    def record_app_usage(self, app_name, category=None):
        """Ghi nhận sử dụng app."""
        if self.analytics_service:
            self.analytics_service.record_app_usage(app_name, category)
