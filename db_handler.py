import datetime
import sqlite3


def create_database() -> None:
    """Create a database"""

    with sqlite3.connect('manicure_users.db') as connection:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                username TEXT NULL,
                full_name TEXT NOT NULL,
                info TEXT NULL,
                datetime TEXT NOT NULL
            )
        ''')

        connection.commit()


def add_user_by_start(telegram_id: int, username: str, full_name: str) -> None:
    """Add a new user to the database"""

    with sqlite3.connect('manicure_users.db') as connection:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO users (telegram_id, username, full_name, datetime) VALUES (?, ?, ?, ?)',
                       (telegram_id, username, full_name, datetime.datetime.utcnow().isoformat()))

        connection.commit()


def check_user_by_id(telegram_id: int):
    """Check if a user exists in the database by their Telegram ID"""

    with sqlite3.connect('manicure_users.db') as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,))
        result = cursor.fetchone()
        return result[0] if result else None


def update_user_info(telegram_id: int, info: str) -> None:
    """Update user information in the database"""

    with sqlite3.connect('manicure_users.db') as connection:
        cursor = connection.cursor()
        cursor.execute('UPDATE users SET info = ? WHERE telegram_id = ?', (info, telegram_id))

        connection.commit()


def remove_table():
    """Remove all table from the database"""

    with sqlite3.connect('manicure_users.db') as connection:
        cursor = connection.cursor()
        cursor.execute('DROP TABLE users')

        connection.commit()
