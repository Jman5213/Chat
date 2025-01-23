import sqlite3
import hashlib
from os import urandom
from base64 import b64encode


################################################################################
#                              HASHING FUNCTIONS                               #
################################################################################


def generate_salt() ->bytes:
    # 128 bit salt value
    salt = urandom(16)
    return salt


def hash_password(password: str, salt = None) -> tuple[str, bytes, str, int]:
    if salt is None:
        salt = generate_salt()
    iterations = 100_000
    function = "pbkdf2_hmac"
    hash_value = b64encode(
        hashlib.pbkdf2_hmac(
            "sha512",
            password.encode("utf-8"),
            salt,
            iterations
        )
    ).decode("utf-8")
    return_value = (hash_value, salt, function, iterations)
    return return_value


################################################################################
#                        STANDARD, MULTI-USE FUNCTIONS                         #
################################################################################


def get_connection():
    """Simply returns the database connection"""
    conn = sqlite3.connect("server.db", check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def exists(table: str, value: str) -> bool:
    """
    :param table: clients or chatrooms
    :param value: value being tested
    :return: true if item exists, false otherwise
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        if table == "clients":
            column = "username"
        elif table == "chatrooms":
            column = "chat_name"
        else:
            return False


        query = f"SELECT  1 FROM {table} WHERE {column} = ? LIMIT 1;"
        cursor.execute(query, (value,))
        result = cursor.fetchone()
        return True if result else False
    finally:
        if conn:
            conn.close()


################################################################################
#                                DB FUNCTIONS                                  #
################################################################################


def init_db() -> bool :
    """
    This function initializes the database
    Prints a string describing success or errors
    Returns: True/False
    """
    conn = None
    try:
        conn = get_connection()
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
                salt BLOB NOT NULL,
                hash_algo TEXT NOT NULL,
                iterations INTEGER NOT NULL
            )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS chatrooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_name TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients_chatroom (
                user_id INTEGER NOT NULL,
                chatroom_id INTEGER NOT NULL,
                PRIMARY KEY (user_id, chatroom_id),
                FOREIGN KEY (user_id) REFERENCES clients(user_id),
                FOREIGN KEY (chatroom_id) REFERENCES chatrooms(id)
            )
        ''')

        conn.commit()
        print("Database initialized")
        return True
    except sqlite3.OperationalError as e:
        print(f"Database operational error: {e}")
        return False
    except Exception as e:
        print(f"Database initialization error: {e}")
        return False
    finally:
        if conn is not None:
            conn.close()


def add_user(username: str, password_plaintext: str) -> bool | None:
    """
    This function adds a user to the database
    :param password_plaintext:
    :param username: username of the user
    :return: True/False, None if an error occurred
    """
    conn = None
    try:
        password, salt, hash_algo, iterations = hash_password(password_plaintext)
    except ValueError as e:
        print(f"Password hashing error: {e}")
        return None

    try:
        if not username or not password:
            print("Username or password is empty")
            return False
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO clients(username, password, salt, hash_algo, iterations)
        VALUES(?, ?, ?, ?, ?)
        ''', (username, password, salt, hash_algo, iterations))
        conn.commit()
        print(f"User [{username}] successfully added")
        return True
    except sqlite3.OperationalError as e:
        print(f"Database initialization error: {e}")
        return None
    except sqlite3.IntegrityError:
        print("Database integrity error: Username already exists")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        if conn is not None:
            conn.close()


def confirm_login(username: str, password_plaintext: str) -> bool | None:
    """
    This function confirms the login of a user
    :param username: username the user entered
    :param password_plaintext: password the user entered
    :return:True/False, None if an error occurred
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT password, salt, hash_algo, iterations
            FROM clients
            WHERE username = ?
        ''', (username,))

        row = cursor.fetchone()
        if row is None:
            print(f"User [{username}] does not exist")
            return False
        stored_password, salt, hash_algo, iterations = row

        if hash_algo == "pbkdf2_hmac":
            hashed_password = hash_password(password_plaintext, salt=salt)[0]
            if hashed_password == stored_password:
                print("Successful login")
                return True
            else:
                print("Wrong password")
                return False
        else:
            print(f"Error: [{hash_algo}] is not supported")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        if conn is not None:
            conn.close()


def