import sqlite3
import uuid

from src.domain.ports import SQLitePort
import logging

logger = logging.getLogger(__name__)

_CREATE_CONVERSATIONS = """
CREATE TABLE IF NOT EXISTS conversations (
    id          TEXT PRIMARY KEY,
    paper_id    TEXT NOT NULL,
    user_id     TEXT NOT NULL,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

_CREATE_MESSAGES = """
CREATE TABLE IF NOT EXISTS messages (
    id              TEXT PRIMARY KEY,
    conversation_id TEXT NOT NULL REFERENCES conversations(id),
    role            TEXT NOT NULL,
    content         TEXT NOT NULL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

_CREATE_PAPERS = """
CREATE TABLE IF NOT EXISTS papers (
    id         TEXT PRIMARY KEY,
    user_id    TEXT NOT NULL,
    title      TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)"""


class SQLiteConversationRepository(SQLitePort):
    """SQLite implementation of SQLitePort for conversation persistence."""

    def __init__(self, db_path: str):
        self._db_path = db_path
        with sqlite3.connect(self._db_path) as conn:
            conn.execute(_CREATE_CONVERSATIONS)
            conn.execute(_CREATE_MESSAGES)
            conn.execute(_CREATE_PAPERS)

    def create_conversation(self, user_id: str, paper_id: str) -> str:
        """Creates a new conversation and returns its ID.

        Args:
            user_id (str): ID of the user starting the conversation.
            paper_id (str): ID of the paper being discussed.

        Returns:
            str: the new conversation ID.
        """
        conversation_id = str(uuid.uuid4())
        with sqlite3.connect(self._db_path) as conn:
            conn.execute(
                "INSERT INTO conversations (id, paper_id, user_id) VALUES (?, ?, ?)",
                (conversation_id, paper_id, user_id),
            )
        logger.info(f"SQLite | Created conversation {conversation_id}")
        return conversation_id

    def add_message(self, conversation_id: str, role: str, content: str) -> None:
        """Inserts a message into the conversation history.

        Args:
            conversation_id (str): ID of the conversation.
            role (str): 'user' or 'assistant'.
            content (str): message text.
        """
        with sqlite3.connect(self._db_path) as conn:
            conn.execute(
                "INSERT INTO messages (id, conversation_id, role, content) VALUES (?, ?, ?, ?)",
                (str(uuid.uuid4()), conversation_id, role, content),
            )
        logger.info(
            f"SQLite | Inserted {role} message in conversation {conversation_id}"
        )

    def get_messages(self, conversation_id: str) -> list[dict]:
        """Retrieves all messages of a conversation ordered by time.

        Args:
            conversation_id (str): ID of the conversation.

        Returns:
            list[dict]: list of messages with 'role' and 'content' keys.
        """
        with sqlite3.connect(self._db_path) as conn:
            rows = conn.execute(
                "SELECT role, content FROM messages WHERE conversation_id = ? ORDER BY created_at ASC",
                (conversation_id,),
            ).fetchall()
        logger.info(
            f"SQLite | Retrieved {len(rows)} messages for conversation {conversation_id}"
        )
        return [{"role": row[0], "content": row[1]} for row in rows]

    def get_paper_id(self, conversation_id: str) -> str:
        """Retrieves the paper_id associated with a conversation.

        Args:
            conversation_id (str): ID of the conversation.

        Returns:
            str: the paper_id.
        """
        with sqlite3.connect(self._db_path) as conn:
            row = conn.execute(
                "SELECT paper_id FROM conversations WHERE id = ?",
                (conversation_id,),
            ).fetchone()
        if row is None:
            raise ValueError(f"Conversation {conversation_id} not found")
        return row[0]
    
    def add_paper(self, paper_id: str, user_id: str, title: str) -> None:
        """Saves a paper's metadata to SQLite.

        Args:
            paper_id (str): unique paper ID.
            user_id (str): ID of the user who indexed the paper.
            title (str): title of the paper.
        """
        with sqlite3.connect(self._db_path) as conn:
            conn.execute(
                "INSERT OR IGNORE INTO papers (id, user_id, title) VALUES (?, ?, ?)",
                (paper_id, user_id, title),
            )
        logger.info(f"SQLite | Saved paper {paper_id} - {title}")

    def get_papers(self, user_id: str) -> list[dict]:
        """Retrieves all papers indexed by a user.

        Args:
            user_id (str): ID of the user.

        Returns:
            list[dict]: list of papers with 'id' and 'title' keys.
        """
        with sqlite3.connect(self._db_path) as conn:
            rows = conn.execute(
                "SELECT id, title FROM papers WHERE user_id = ? ORDER BY created_at DESC",
                (user_id,),
            ).fetchall()
        return [{"id": row[0], "title": row[1]} for row in rows]
        
