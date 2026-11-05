"""
Unb0und-AI Persistent Memory

Stores conversations and messages in a local SQLite database.
"""

import sqlite3
from pathlib import Path
from datetime import datetime


# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database location
DATABASE_PATH = BASE_DIR / "data" / "unb0und_memory.db"


def get_connection():
    """
    Connect to the SQLite database.
    """

    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    return connection


def initialize_database():
    """
    Create database tables if they do not exist.
    """

    with get_connection() as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL,

                FOREIGN KEY (conversation_id)
                REFERENCES conversations(id)
                ON DELETE CASCADE
            )
        """)

    print("Memory database initialized.")


def create_conversation(title="New Conversation"):
    """
    Create a new conversation.

    Returns the conversation ID.
    """

    with get_connection() as connection:

        cursor = connection.execute(
            """
            INSERT INTO conversations (title, created_at)
            VALUES (?, ?)
            """,
            (
                title,
                datetime.now().isoformat(
                    timespec="seconds"
                )
            )
        )

        return cursor.lastrowid


def save_message(conversation_id, role, content):
    """
    Save a message to an existing conversation.
    """

    if role not in ("user", "assistant", "system"):
        raise ValueError("Invalid message role.")

    with get_connection() as connection:

        connection.execute(
            """
            INSERT INTO messages (
                conversation_id,
                role,
                content,
                created_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                conversation_id,
                role,
                content,
                datetime.now().isoformat(
                    timespec="seconds"
                )
            )
        )


def get_messages(conversation_id, limit=20):
    """
    Retrieve recent messages in chronological order.
    """

    with get_connection() as connection:

        rows = connection.execute(
            """
            SELECT role, content, created_at
            FROM (
                SELECT id, role, content, created_at
                FROM messages
                WHERE conversation_id = ?
                ORDER BY id DESC
                LIMIT ?
            )
            ORDER BY id ASC
            """,
            (
                conversation_id,
                limit
            )
        ).fetchall()

        return [
            dict(row)
            for row in rows
        ]


def list_conversations():
    """
    Return all conversations, newest first.
    """

    with get_connection() as connection:

        rows = connection.execute(
            """
            SELECT id, title, created_at
            FROM conversations
            ORDER BY id DESC
            """
        ).fetchall()

        return [
            dict(row)
            for row in rows
        ]


def delete_conversation(conversation_id):
    """
    Delete a conversation and its messages.
    """

    with get_connection() as connection:

        cursor = connection.execute(
            """
            DELETE FROM conversations
            WHERE id = ?
            """,
            (conversation_id,)
        )

        return cursor.rowcount > 0