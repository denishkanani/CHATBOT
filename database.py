import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_name="research.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        """
        Create database tables if they don't exist.
        """

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            source TEXT,
            created_at TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT,
            created_at TEXT
        )
        """)

        self.connection.commit()

    # -----------------------------
    # Documents
    # -----------------------------

    def add_document(self, doc_id, title, source):
        self.cursor.execute("""
        INSERT OR REPLACE INTO documents
        (id, title, source, created_at)
        VALUES (?, ?, ?, ?)
        """, (
            doc_id,
            title,
            source,
            datetime.now().isoformat()
        ))

        self.connection.commit()

    def get_documents(self):
        self.cursor.execute("SELECT * FROM documents")
        return self.cursor.fetchall()

    def get_document(self, doc_id):
        self.cursor.execute(
            "SELECT * FROM documents WHERE id=?",
            (doc_id,)
        )
        return self.cursor.fetchone()

    def delete_document(self, doc_id):
        self.cursor.execute(
            "DELETE FROM documents WHERE id=?",
            (doc_id,)
        )
        self.connection.commit()

    # -----------------------------
    # Search History
    # -----------------------------

    def save_search(self, question, answer):
        self.cursor.execute("""
        INSERT INTO search_history
        (question, answer, created_at)
        VALUES (?, ?, ?)
        """, (
            question,
            answer,
            datetime.now().isoformat()
        ))

        self.connection.commit()

    def get_search_history(self):
        self.cursor.execute("""
        SELECT * FROM search_history
        ORDER BY id DESC
        """)

        return self.cursor.fetchall()

    def close(self):
        self.connection.close()


if __name__ == "__main__":

    db = Database()

    db.add_document(
        "1",
        "Artificial Intelligence",
        "Wikipedia"
    )

    db.save_search(
        "What is AI?",
        "Artificial Intelligence is the simulation of human intelligence."
    )

    print("Documents")
    print(db.get_documents())

    print("\nSearch History")
    print(db.get_search_history())

    db.close()