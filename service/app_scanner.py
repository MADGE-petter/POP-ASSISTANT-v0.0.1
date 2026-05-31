"""App Scanner - Tìm kiếm ứng dụng đã cài đặt trên hệ thống."""

import os
import platform
from pathlib import Path


class AppScanner:
    """Quét và tìm kiếm ứng dụng đã cài đặt."""
    
    def __init__(self):
        self.app_cache = {}
        self._scan_common_apps()
    
    def _scan_common_apps(self):
        """Quét các ứng dụng phổ biến."""
        if platform.system() == "Windows":
            self._scan_windows_apps()
        elif platform.system() == "Darwin":
            self._scan_mac_apps()
        else:
            self._scan_linux_apps()
    
    def _scan_windows_apps(self):
        """Quét ứng dụng trên Windows."""
        # Các đường dẫn phổ biến
        program_dirs = [
            os.environ.get('PROGRAMFILES', 'C:\\Program Files'),
            os.environ.get('PROGRAMFILES(X86)', 'C:\\Program Files (x86)'),
            os.environ.get('LOCALAPPDATA', ''),
        ]
        
        # Ứng dụng phổ biến
        common_apps = {
            'chrome': ['Google\\Chrome\\Application\\chrome.exe'],
            'firefox': ['Mozilla Firefox\\firefox.exe'],
            'edge': ['Microsoft\\Edge\\Application\\msedge.exe'],
            'word': ['Microsoft Office\\root\\Office16\\WINWORD.EXE', 'Microsoft Office\\Office16\\WINWORD.EXE'],
            'excel': ['Microsoft Office\\root\\Office16\\EXCEL.EXE', 'Microsoft Office\\Office16\\EXCEL.EXE'],
            'notepad': ['notepad.exe'],
            'calculator': ['calc.exe'],
            'zalo': ['Zalo\\Zalo.exe'],
            'code': ['Microsoft VS Code\\Code.exe', 'vscode\\Code.exe'],
        }
        
        for app_name, paths in common_apps.items():
            for path in paths:
                if path.endswith('.exe') and '\\' not in path:
                    # System command
                    self.app_cache[app_name] = path
                    break
                full_path = os.path.join(os.environ.get('PROGRAMFILES', 'C:\\Program Files'), path)
                if os.path.exists(full_path):
                    self.app_cache[app_name] = full_path
                    break
                full_path_x86 = os.path.join(os.environ.get('PROGRAMFILES(X86)', 'C:\\Program Files (x86)'), path)
                if os.path.exists(full_path_x86):
                    self.app_cache[app_name] = full_path_x86
                    break
    
    def _scan_mac_apps(self):
        """Quét ứng dụng trên macOS."""
        app_dirs = ['/Applications', str(Path.home() / 'Applications')]
        for app_dir in app_dirs:
            if os.path.exists(app_dir):
                try:
                    for item in os.listdir(app_dir):
                        if item.endswith('.app'):
                            app_name = item.replace('.app', '').lower()
                            self.app_cache[app_name] = os.path.join(app_dir, item)
                except:
                    pass
    
    def _scan_linux_apps(self):
        """Quét ứng dụng trên Linux."""
        # Đọc từ .desktop files
        app_dirs = ['/usr/share/applications', str(Path.home() / '.local/share/applications')]
        for app_dir in app_dirs:
            if os.path.exists(app_dir):
                try:
                    for item in os.listdir(app_dir):
                        if item.endswith('.desktop'):
                            app_name = item.replace('.desktop', '').lower()
                            self.app_cache[app_name] = os.path.join(app_dir, item)
                except:
                    pass
    
    def find_app(self, app_name):
       
        app_name_lower = app_name.lower().strip()
        
        # Tìm trong cache trước
        for cached_name, cached_path in self.app_cache.items():
            if app_name_lower in cached_name or cached_name in app_name_lower:
                return cached_name, cached_path
        
        # Thử tìm với các biến thể tên
        variations = [
            app_name_lower,
            app_name_lower.replace(' ', ''),
            app_name_lower.replace('-', ''),
            app_name_lower.replace('_', ''),
        ]
        
        for variant in variations:
            for cached_name, cached_path in self.app_cache.items():
                if variant in cached_name:
                    return cached_name, cached_path
        
        return None, None
