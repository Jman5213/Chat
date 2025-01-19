import sqlite3

from pyasn1.type.univ import Boolean


def init_db() -> bool :
    """
    This function initializes the database
    Prints a string describing success or errors
    Returns: True/False
    """
    conn = None
    try:
        conn = sqlite3.connect("server.db", check_same_thread=False)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id TEXT NOT NULL,
                username TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                salt TEXT NOT NULL,
                hash_algo TEXT NOT NULL,
                iterations INTEGER NOT NULL,
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients_chatroom (
                user_id INTEGER NOT NULL,
                chatroom_id INTEGER NOT NULL,
                PRIMARY KEY (user_id, chatroom_id),
                FOREIGN KEY (user_id) REFERENCES clients(id),
                FOREIGN KEY (chatroom_id) REFERENCES chatrooms(id)
            )
        ''')

        conn.commit()
        print("Database initialized")
    except sqlite3.OperationalError:
        print("Database initialization error")
    except Exception as e:
        print(f"Database initialization error: {e}")
    finally:
        if conn is not None:
            conn.close()
            return True
        else:
            return False


def add_user(username: str, password: str, salt: str, hash_algo: str, iterations: int):
    conn = None
    try:
        conn = sqlite3.connect("server.db", check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO clients(username, password, salt, hash_algo, iterations)
        VALUES(?, ?, ?, ?, ?)
        ''', (username, password, salt, hash_algo, iterations))
        conn.commit()
    except sqlite3.OperationalError:
        print("Database initialization error")
    except sqlite3.IntegrityError:
        print("Database integrity error: Username already exists")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn is not None:
            conn.close()


