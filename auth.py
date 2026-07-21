import sqlite3
import bcrypt


class Auth:
    def __init__(self, db_name="research.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_users_table()

    def create_users_table(self):
        """
        Create users table.
        """
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """)
        self.connection.commit()

    def register(self, username, password):
        """
        Register a new user.
        """
        try:
            hashed_password = bcrypt.hashpw(
                password.encode(),
                bcrypt.gensalt()
            ).decode()

            self.cursor.execute("""
            INSERT INTO users (username, password)
            VALUES (?, ?)
            """, (username, hashed_password))

            self.connection.commit()

            return True, "User registered successfully."

        except sqlite3.IntegrityError:
            return False, "Username already exists."

    def login(self, username, password):
        """
        Verify login credentials.
        """
        self.cursor.execute("""
        SELECT password
        FROM users
        WHERE username = ?
        """, (username,))

        row = self.cursor.fetchone()

        if row is None:
            return False, "User not found."

        stored_password = row[0]

        if bcrypt.checkpw(
            password.encode(),
            stored_password.encode()
        ):
            return True, "Login successful."

        return False, "Invalid password."

    def list_users(self):
        """
        Return all registered users.
        """
        self.cursor.execute("""
        SELECT id, username
        FROM users
        """)

        return self.cursor.fetchall()

    def close(self):
        self.connection.close()


if __name__ == "__main__":

    auth = Auth()

    print(auth.register("admin", "password123"))
    print(auth.login("admin", "password123"))
    print(auth.list_users())

    auth.close()