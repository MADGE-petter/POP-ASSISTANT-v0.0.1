import os
import sqlite3
from datetime import datetime

from utils.logger import get_logger

from .base_repository import BaseRepository

logger = get_logger(__name__)

class ConversationDB(BaseRepository):
    """Database operations for conversations"""

    def __init__(self, db_path: str = None):
        if db_path:
            resolved = db_path
        else:
            resolved = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'conversations.db')
        super().__init__(resolved)
        self.init_database()
    
    def init_database(self):
        """Initialize database tables if they don't exist"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            if not tables:
                self._create_default_schema(cursor)
                conn.commit()
                logger.info("Created default conversation DB schema for %s", self.db_path)
            
            conn.close()
        except Exception as e:
            logger.error("Database initialization error: %s", e, exc_info=True)
            raise

    def _create_default_schema(self, cursor):
        """Create the default schema required for the conversation database."""
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                maNguoiDung INTEGER PRIMARY KEY AUTOINCREMENT,
                tenNguoiDung TEXT NOT NULL UNIQUE,
                matKhauMaHoa TEXT,
                hoTen TEXT,
                thoiGianTao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                thoiGianCapNhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin_users (
                maAdmin INTEGER PRIMARY KEY AUTOINCREMENT,
                tenAdmin TEXT NOT NULL UNIQUE,
                matKhauMaHoa TEXT NOT NULL,
                thoiGianTao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                thoiGianCapNhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                maPhien TEXT PRIMARY KEY,
                maNguoiDung INTEGER,
                thoiGianBatDau TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                thoiGianKetThuc TIMESTAMP,
                FOREIGN KEY (maNguoiDung) REFERENCES users(maNguoiDung) ON DELETE SET NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                maCuocTroChuyen INTEGER PRIMARY KEY AUTOINCREMENT,
                maPhien TEXT NOT NULL,
                maNguoiDung INTEGER,
                tinNhanCuaKhach TEXT NOT NULL,
                tinNhanCuaBot TEXT NOT NULL,
                thoiGianTao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                loaiYDo TEXT,
                FOREIGN KEY (maPhien) REFERENCES sessions(maPhien) ON DELETE CASCADE,
                FOREIGN KEY (maNguoiDung) REFERENCES users(maNguoiDung) ON DELETE SET NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_settings (
                maCaiDat INTEGER PRIMARY KEY AUTOINCREMENT,
                maNguoiDung INTEGER NOT NULL,
                khoaCaiDat TEXT NOT NULL,
                giaTriCaiDat TEXT,
                thoiGianTao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (maNguoiDung) REFERENCES users(maNguoiDung) ON DELETE CASCADE,
                UNIQUE(maNguoiDung, khoaCaiDat)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usage_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                start_time TEXT,
                end_time TEXT,
                duration_seconds INTEGER,
                tenNguoiDung TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS app_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                timestamp TEXT,
                app_name TEXT,
                action TEXT,
                tenNguoiDung TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS health_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                timestamp TEXT,
                cpu_percent REAL,
                ram_percent REAL,
                disk_percent REAL,
                temperature REAL,
                tenNguoiDung TEXT
            )
        """)

        cursor.execute("CREATE INDEX IF NOT EXISTS idx_conversations_maNguoiDung ON conversations(maNguoiDung)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_conversations_maPhien ON conversations(maPhien)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_conversations_thoiGianTao ON conversations(thoiGianTao)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_maNguoiDung ON sessions(maNguoiDung)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_thoiGianBatDau ON sessions(thoiGianBatDau)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_tenNguoiDung ON users(tenNguoiDung)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_usage_sessions_date ON usage_sessions(date)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_usage_sessions_user ON usage_sessions(tenNguoiDung)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_app_usage_date ON app_usage(date)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_app_usage_user ON app_usage(tenNguoiDung)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_health_snapshots_date ON health_snapshots(date)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_health_snapshots_user ON health_snapshots(tenNguoiDung)")

        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS update_users_timestamp 
            AFTER UPDATE ON users
            BEGIN
                UPDATE users SET thoiGianCapNhat = CURRENT_TIMESTAMP WHERE maNguoiDung = NEW.maNguoiDung;
            END
        """)

        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS update_admin_users_timestamp 
            AFTER UPDATE ON admin_users
            BEGIN
                UPDATE admin_users SET thoiGianCapNhat = CURRENT_TIMESTAMP WHERE maAdmin = NEW.maAdmin;
            END
        """)
    
    def save_conversation(self, user_id, session_id, user_message, bot_response, intent_type=None):
        """Save a conversation to database"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Debug: Log what we're saving
            logger.debug("Saving conversation: user=%s (type=%s), session=%s (type=%s)", user_id, type(user_id).__name__, session_id, type(session_id).__name__)
            
            cursor.execute("""
                INSERT INTO conversations (maNguoiDung, maPhien, tinNhanCuaKhach, tinNhanCuaBot, loaiYDo)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, session_id, user_message, bot_response, intent_type))
            
            conn.commit()
            last_id = cursor.lastrowid
            conn.close()
            logger.info("Saved conversation, rowid=%s", last_id)
            
        except Exception as e:
            logger.error("Error saving conversation: %s", e, exc_info=True)
    
    def get_conversations(self, user_id=None, limit=50):
        """Get conversations from database"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            if user_id:
                cursor.execute("""
                    SELECT c.*, u.tenNguoiDung, u.hoTen 
                    FROM conversations c
                    JOIN users u ON c.maNguoiDung = u.maNguoiDung
                    WHERE c.maNguoiDung = ?
                    ORDER BY c.thoiGianTao DESC
                    LIMIT ?
                """, (user_id, limit))
            else:
                cursor.execute("""
                    SELECT c.*, u.tenNguoiDung, u.hoTen 
                    FROM conversations c
                    JOIN users u ON c.maNguoiDung = u.maNguoiDung
                    ORDER BY c.thoiGianTao DESC
                    LIMIT ?
                """, (limit,))
            
            result = cursor.fetchall()
            conn.close()
            
            return result
            
        except Exception as e:
            logger.error("Error getting conversations: %s", e, exc_info=True)
            return []
    
    def get_user_by_username(self, username):
        """Get user by username"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM users WHERE tenNguoiDung = ?", (username,))
            result = cursor.fetchone()
            conn.close()
            
            return result
            
        except Exception as e:
            logger.error("Error getting user: %s", e, exc_info=True)
            return None
    
    def create_user(self, username, email=None):
        """Create a new user"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Schema không có cột email, chỉ insert tenNguoiDung
            cursor.execute("""
                INSERT INTO users (tenNguoiDung)
                VALUES (?)
            """, (username,))
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return user_id
            
        except Exception as e:
            logger.error("Error creating user: %s", e, exc_info=True)
            return None
    
    def get_or_create_user(self, username):
        """Get existing user or create new one"""
        user = self.get_user_by_username(username)
        if user:
            return user[0]  # user_id
        else:
            return self.create_user(username)
    
    def start_session(self, user_id: int = None) -> int:
        """Bắt đầu session mới và trả về session ID (integer)."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Nếu user_id là string, convert sang int nếu có thể
            if isinstance(user_id, str) and user_id.isdigit():
                user_id = int(user_id)
            elif user_id is None or (isinstance(user_id, str) and not user_id.isdigit()):
                # Guest user - lấy user đầu tiên hoặc tạo guest
                user_id = 1  # Default to first user
            
            cursor.execute("""
                INSERT INTO sessions (maNguoiDung, thoiGianBatDau)
                VALUES (?, ?)
            """, (user_id, datetime.now()))
            
            session_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return session_id
            
        except Exception as e:
            logger.error("Error starting session: %s", e, exc_info=True)
            return 1  # Return default session ID on error
    
    def end_session(self, session_id):
        """End a session"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE sessions 
                SET thoiGianKetThuc = ?
                WHERE maPhien = ?
            """, (datetime.now(), session_id))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error("Error ending session: %s", e, exc_info=True)
    
    def get_user_sessions(self, user_id, limit=20):
        """Get sessions for a user"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM sessions 
                WHERE maNguoiDung = ?
                ORDER BY thoiGianBatDau DESC
                LIMIT ?
            """, (user_id, limit))
            
            result = cursor.fetchall()
            conn.close()
            
            return result
            
        except Exception as e:
            logger.error("Error getting sessions: %s", e, exc_info=True)
            return []
    
    def get_session_conversations(self, session_id, username=None):
        """Get conversations for a session"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            if username:
                cursor.execute("""
                    SELECT c.tinNhanCuaKhach, c.tinNhanCuaBot, c.thoiGianTao
                    FROM conversations c
                    JOIN sessions s ON c.maPhien = s.maPhien
                    JOIN users u ON s.maNguoiDung = u.maNguoiDung
                    WHERE c.maPhien = ? AND u.tenNguoiDung = ?
                    ORDER BY c.thoiGianTao ASC
                """, (session_id, username))
            else:
                cursor.execute("""
                    SELECT tinNhanCuaKhach, tinNhanCuaBot, thoiGianTao
                    FROM conversations 
                    WHERE maPhien = ?
                    ORDER BY thoiGianTao ASC
                """, (session_id,))
            
            result = cursor.fetchall()
            conn.close()
            
            return result
            
        except Exception as e:
            logger.error("Error getting session conversations: %s", e, exc_info=True)
            return []
    
    def get_all_sessions(self, username, limit=30):
        """Get all sessions for a username"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT s.maPhien, s.thoiGianBatDau, s.thoiGianKetThuc
                FROM sessions s
                JOIN users u ON s.maNguoiDung = u.maNguoiDung
                WHERE u.tenNguoiDung = ?
                ORDER BY s.thoiGianBatDau DESC
                LIMIT ?
            """, (username, limit))

            result = cursor.fetchall()
            conn.close()

            return result

        except Exception as e:
            logger.error("Error getting all sessions: %s", e, exc_info=True)
            return []
    
    def get_statistics(self, user_id):
        """Get statistics for a user"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT COUNT(*) as total_conversations,
                       COUNT(DISTINCT DATE(thoiGianTao)) as total_days,
                       COUNT(DISTINCT maPhien) as total_sessions
                FROM conversations 
                WHERE maNguoiDung = ?
            """, (user_id,))

            result = cursor.fetchone()
            conn.close()

            return result if result else (0, 0, 0)

        except Exception as e:
            logger.error("Error getting statistics: %s", e, exc_info=True)
            return (0, 0, 0)
    
    def get_daily_statistics(self, user_id, limit=30):
        """Get daily statistics for a user"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT DATE(thoiGianTao) as date,
                       COUNT(*) as conversation_count,
                       COUNT(DISTINCT maPhien) as session_count
                FROM conversations 
                WHERE maNguoiDung = ?
                GROUP BY DATE(thoiGianTao)
                ORDER BY date DESC
                LIMIT ?
            """, (user_id, limit))

            result = cursor.fetchall()
            conn.close()

            return result

        except Exception as e:
            logger.error("Error getting daily statistics: %s", e, exc_info=True)
            return []
    
    def delete_old_conversations(self, days=30):
        """Delete conversations older than specified days"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                DELETE FROM conversations 
                WHERE thoiGianTao < datetime('now', '-{} days')
            """.format(days))
            
            deleted_count = cursor.rowcount
            conn.commit()
            conn.close()
            
            logger.info("Deleted %s old conversations", deleted_count)
            
        except Exception as e:
            logger.error("Error deleting old conversations: %s", e, exc_info=True)
    
    def get_display_name(self, user_id):
        """Lấy họ tên (tên hiển thị) của user"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT hoTen FROM users WHERE maNguoiDung = ?", (user_id,))
            result = cursor.fetchone()
            conn.close()

            return result[0] if result and result[0] else None
        except Exception as e:
            logger.error("Error getting display name: %s", e, exc_info=True)
            return None
    
    def update_display_name(self, user_id, display_name):
        """Cập nhật họ tên (tên hiển thị) cho user"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE users 
                SET hoTen = ?, thoiGianCapNhat = CURRENT_TIMESTAMP
                WHERE maNguoiDung = ?
            """, (display_name, user_id))

            conn.commit()
            conn.close()
            logger.info("Updated display name for user %s to: %s", user_id, display_name)
            return True
        except Exception as e:
            logger.error("Error updating display name: %s", e, exc_info=True)
            return False
