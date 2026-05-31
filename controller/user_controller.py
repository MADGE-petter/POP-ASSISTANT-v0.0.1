"""User Controller - Quản lý user data và session."""

from typing import Optional

from controller.interfaces import ISqlService, IUserService


class UserController:
    def __init__(self, user_service: IUserService, sql_service: ISqlService):
        self.user_service = user_service
        self.sql_service = sql_service
        self.login_username: Optional[str] = None
    
    def set_login_username(self, username):
        """Thiết lập username đăng nhập."""
        self.login_username = username
        if username:
            self.user_service.login_name = username
            self.user_service.display_name = self.user_service.get_display_name_by_login(username)
            print(f"[UserController] Loaded user: login={username}, display={self.user_service.display_name}")
    
    def get_display_name(self):
        """Lấy tên hiển thị."""
        return self.user_service.get_user_name()
    
    def get_login_name(self):
        """Lấy tên đăng nhập."""
        return self.user_service.login_name
    
    def update_user_name(self, new_name):
        """Cập nhật tên người dùng."""
        return self.user_service.update_user_name(
            new_name,
            self.sql_service.current_session_id
        )
    
    def is_name_known(self):
        """Kiểm tra đã biết tên user chưa."""
        return self.user_service.is_name_known()
