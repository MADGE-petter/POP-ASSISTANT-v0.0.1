"""Admin Repository - Quản lý dữ liệu admin từ database."""
import os
import sqlite3
from typing import Dict, List, Optional

from utils.logger import get_logger

from .base_repository import BaseRepository

logger = get_logger(__name__)


class AdminRepository(BaseRepository):
    """Repository cho admin data - kế thừa BaseRepository."""

    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = os.path.join(
                os.path.dirname(__file__), 'conversations.db'
            )
        super().__init__(db_path)
        self._init_admin_tables()

    def _init_admin_tables(self):
        """Khởi tạo bảng admin_users và system_logs."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            # Bảng admin_users
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS admin_users (
                    maAdmin INTEGER PRIMARY KEY AUTOINCREMENT,
                    tenAdmin TEXT NOT NULL UNIQUE,
                    matKhauMaHoa TEXT NOT NULL,
                    email TEXT,
                    thoiGianTao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    thoiGianCapNhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Bảng system_logs
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_logs (
                    maLog INTEGER PRIMARY KEY AUTOINCREMENT,
                    level TEXT,
                    message TEXT,
                    module TEXT,
                    thoiGianTao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.commit()
            conn.close()

        except Exception as e:
            logger.error("Error initializing admin tables: %s", e, exc_info=True)

    def verify_admin_login(self, username: str, password_hash: str) -> Optional[Dict]:
        """Xác thực admin login."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT maAdmin, tenAdmin, email
                FROM admin_users
                WHERE tenAdmin = ? AND matKhauMaHoa = ?
            """, (username, password_hash))

            result = cursor.fetchone()
            conn.close()

            if result:
                return {
                    'id': result['maAdmin'],
                    'username': result['tenAdmin'],
                    'email': result['email'],
                    'role': 'admin'
                }
            return None

        except Exception as e:
            logger.error("Error verifying admin login: %s", e, exc_info=True)
            return None

    def get_admin_password_hash(self, username: str = 'admin') -> Optional[str]:
        """Return stored password hash for admin user."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT matKhauMaHoa FROM admin_users WHERE tenAdmin = ?", (username,))
            row = cursor.fetchone()
            conn.close()
            return row['matKhauMaHoa'] if row and 'matKhauMaHoa' in row.keys() else None
        except Exception as e:
            logger.error("Error getting admin password hash: %s", e, exc_info=True)
            return None

    def update_admin_password(self, username: str, password_hash: str) -> bool:
        """Update admin password hash."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE admin_users SET matKhauMaHoa = ?, thoiGianCapNhat = CURRENT_TIMESTAMP WHERE tenAdmin = ?", (password_hash, username))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error("Error updating admin password: %s", e, exc_info=True)
            return False

    def get_active_sessions_count(self) -> int:
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as cnt FROM sessions WHERE thoiGianKetThuc IS NULL")
            row = cursor.fetchone()
            conn.close()
            return int(row['cnt']) if row and 'cnt' in row.keys() else 0
        except Exception as e:
            logger.error("Error getting active sessions count: %s", e, exc_info=True)
            return 0

    def get_app_usage_logs_count(self) -> int:
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as cnt FROM app_usage_logs")
            row = cursor.fetchone()
            conn.close()
            return int(row['cnt']) if row and 'cnt' in row.keys() else 0
        except Exception as e:
            logger.error("Error getting app usage logs count: %s", e, exc_info=True)
            return 0

    def get_user_statistics(self) -> Dict:
        """Lấy thống kê người dùng."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM users")
            total_users = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(DISTINCT maNguoiDung)
                FROM conversations
                WHERE thoiGianTao >= datetime('now', '-7 days')
            """)
            active_users_7d = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(DISTINCT maNguoiDung)
                FROM conversations
                WHERE thoiGianTao >= datetime('now', '-30 days')
            """)
            active_users_30d = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM sessions")
            total_sessions = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM conversations")
            total_conversations = cursor.fetchone()[0]

            conn.close()

            return {
                'total_users': total_users or 0,
                'active_users_7d': active_users_7d or 0,
                'active_users_30d': active_users_30d or 0,
                'total_sessions': total_sessions or 0,
                'total_conversations': total_conversations or 0
            }

        except Exception as e:
            logger.error("Error getting user statistics: %s", e, exc_info=True)
            return {}

    def get_conversation_history(
        self, limit: int = 100, offset: int = 0
    ) -> List[Dict]:
        """Lấy lịch sử trò chuyện."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT COALESCE(u.tenNguoiDung, 'Unknown') as tenNguoiDung,
                       COALESCE(c.tinNhanCuaKhach, '') as tinNhanCuaKhach,
                       COALESCE(c.tinNhanCuaBot, '') as tinNhanCuaBot,
                       COALESCE(c.thoiGianTao, datetime('now')) as thoiGianTao,
                       COALESCE(c.maPhien, '') as maPhien
                FROM conversations c
                LEFT JOIN users u ON c.maNguoiDung = u.maNguoiDung
                ORDER BY COALESCE(c.thoiGianTao, datetime('now')) DESC
                LIMIT ? OFFSET ?
            """, (limit, offset))

            columns = ['user_name', 'user_input', 'bot_response', 'created_at', 'session_id']
            results = []

            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))

            conn.close()
            return results

        except Exception as e:
            logger.error("Error getting conversation history: %s", e, exc_info=True)
            return []

    def add_system_log(self, level: str, message: str, module: str) -> bool:
        """Thêm log hệ thống."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO system_logs (level, message, module)
                VALUES (?, ?, ?)
            """, (level, message, module))

            conn.commit()
            conn.close()
            return True

        except Exception as e:
            logger.error("Error adding system log: %s", e, exc_info=True)
            return False

    def cleanup_old_data(self, days: int = 30) -> int:
        """Dọn dẹp dữ liệu cũ."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute(f"""
                DELETE FROM conversations
                WHERE thoiGianTao < datetime('now', '-{days} days')
            """)
            conversations_deleted = cursor.rowcount

            cursor.execute(f"""
                DELETE FROM system_logs
                WHERE thoiGianTao < datetime('now', '-{days} days') AND level = 'INFO'
            """)
            logs_deleted = cursor.rowcount

            conn.commit()
            conn.close()

            total_deleted = conversations_deleted + logs_deleted
            logger.info("Cleaned up %d old records", total_deleted)

            return total_deleted

        except Exception as e:
            logger.error("Error cleaning up old data: %s", e, exc_info=True)
            return 0

    def export_conversations(
        self, start_date: str = None, end_date: str = None
    ) -> List[tuple]:
        """Xuất conversations."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            query = """
                SELECT u.tenNguoiDung, c.tinNhanCuaKhach, c.tinNhanCuaBot,
                       c.thoiGianTao, c.maPhien
                FROM conversations c
                LEFT JOIN users u ON c.maNguoiDung = u.maNguoiDung
            """
            params = []

            if start_date and end_date:
                query += " WHERE c.thoiGianTao BETWEEN ? AND ?"
                params = [start_date, end_date]

            query += " ORDER BY c.thoiGianTao"

            cursor.execute(query, params)
            results = cursor.fetchall()
            conn.close()

            return results

        except Exception as e:
            logger.error("Error exporting conversations: %s", e, exc_info=True)
            return []

    def export_users(self) -> List[tuple]:
        """Xuất danh sách users."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT tenNguoiDung,
                       thoiGianTao,
                       (SELECT MAX(thoiGianTao) FROM conversations
                        WHERE maNguoiDung = u.maNguoiDung) as last_interaction,
                       (SELECT COUNT(*) FROM conversations
                        WHERE maNguoiDung = u.maNguoiDung) as total_interactions
                FROM users u
                ORDER BY thoiGianTao
            """)

            results = cursor.fetchall()
            conn.close()
            return results

        except Exception as e:
            logger.error("Error exporting users: %s", e, exc_info=True)
            return []

    def export_logs(
        self, start_date: str = None, end_date: str = None
    ) -> List[tuple]:
        """Xuất system logs."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            query = "SELECT level, message, module, thoiGianTao FROM system_logs"
            params = []

            if start_date and end_date:
                query += " WHERE thoiGianTao BETWEEN ? AND ?"
                params = [start_date, end_date]

            query += " ORDER BY thoiGianTao"

            cursor.execute(query, params)
            results = cursor.fetchall()
            conn.close()

            return results

        except Exception as e:
            logger.error("Error exporting logs: %s", e, exc_info=True)
            return []
