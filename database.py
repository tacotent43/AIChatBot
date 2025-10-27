from typing import Any, Dict, List, Optional

import aiosqlite

CREATE_MESSAGES_TABLE = """
CREATE TABLE IF NOT EXISTS messages (
id INTEGER PRIMARY KEY AUTOINCREMENT,
chat_id INTEGER NOT NULL,
role TEXT NOT NULL,
content TEXT NOT NULL,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


CREATE_SETTINGS_TABLE = """
CREATE TABLE IF NOT EXISTS settings (
chat_id INTEGER PRIMARY KEY,
style TEXT DEFAULT 'default'
);
"""


class DB:
    def __init__(self, path: str):
        self.path = path
        self._conn: Optional[aiosqlite.Connection] = None

    async def init(self):
        self._conn = await aiosqlite.connect(self.path)
        await self._conn.execute(CREATE_MESSAGES_TABLE)
        await self._conn.execute(CREATE_SETTINGS_TABLE)
        await self._conn.commit()

    async def add_message(self, chat_id: int, role: str, content: str):
        await self._conn.execute(
            "INSERT INTO messages (chat_id, role, content) VALUES (?, ?, ?)",
            (chat_id, role, content),
        )
        await self._conn.commit()

    async def get_recent_messages(self, chat_id: int, limit: int) -> List[Dict[str, Any]]:
        cur = await self._conn.execute(
            "SELECT role, content, created_at FROM messages WHERE chat_id = ? ORDER BY id DESC LIMIT ?",
            (chat_id, limit),
        )
        rows = await cur.fetchall()
        rows.reverse()
        return [{"role": r[0], "content": r[1], "created_at": r[2]} for r in rows]

    async def clear_context(self, chat_id: int):
        await self._conn.execute("DELETE FROM messages WHERE chat_id = ?", (chat_id,))
        await self._conn.commit()

    async def set_style(self, chat_id: int, style: str):
        await self._conn.execute(
            "REPLACE INTO settings(chat_id, style) VALUES (?, ?)", (chat_id, style)
        )
        await self._conn.commit()

    async def get_style(self, chat_id: int) -> str:
        cur = await self._conn.execute("SELECT style FROM settings WHERE chat_id = ?", (chat_id,))
        row = await cur.fetchone()
        return row[0] if row else "default"
