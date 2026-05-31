import sqlite3

from database.conversation_db import ConversationDB


def test_get_connection(tmp_path):
    db_file = tmp_path / "test_conversations.db"
    db = ConversationDB(str(db_file))
    conn = db._get_connection()
    assert isinstance(conn, sqlite3.Connection)
    # simple query to validate connection works
    cur = conn.cursor()
    cur.execute("SELECT 1")
    assert cur.fetchone()[0] == 1
    conn.close()
