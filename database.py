import sqlite3
import hashlib
from os import urandom
from base64 import b64encode
from typing import Optional


CONN = sqlite3.connect("server.db", check_same_thread=False)
CONN.execute("PRAGMA foreign_keys = ON;")


################################################################################
#                              HASHING FUNCTIONS                               #
################################################################################


def generate_salt() ->bytes:
    # 128 bit salt value
    salt = urandom(16)
    return salt


def hash_password(password: str, salt: Optional[bytes] = None) -> tuple[str, bytes, str, int]:
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


def exists(table: str, value: str) -> bool:
    """
    :param table: clients or chatrooms
    :param value: value being tested
    :return: true if item exists, false otherwise
    """
    global CONN
    try:
        cursor = CONN.cursor()

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
        if CONN:
            CONN.close()


################################################################################
#                                DB FUNCTIONS                                  #
################################################################################


def init_db() -> bool :
    """
    This function initializes the database
    Prints a string describing success or errors
    Returns: True/False
    """
    global CONN
    try:
        cursor = CONN.cursor()

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
            chat_name TEXT NOT NULL,
            owner_id INTEGER NOT NULL,
            FOREIGN KEY (owner_id) REFERENCES clients(user_id)
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

        CONN.commit()
        print("Database initialized")
        return True
    except sqlite3.OperationalError as e:
        print(f"Database operational error: {e}")
        return False
    except Exception as e:
        print(f"Database initialization error: {e}")
        return False
    finally:
        if CONN is not None:
            CONN.close()


def add_user(username: str, password_plaintext: str) -> bool | None:
    """
    This function adds a user to the database
    :param password_plaintext: plaintext password to add (stored as a hash)
    :param username: username of the user
    :return: True/False, None if an error occurred
    """
    global CONN
    try:
        password, salt, hash_algo, iterations = hash_password(password_plaintext)
    except ValueError as e:
        print(f"Password hashing error: {e}")
        return None

    try:
        if not username or not password:
            print("Username or password is empty")
            return False
        cursor = CONN.cursor()
        if exists("clients", username):
            print("Database integrity error: Username already exists")
            return False
        else:
            cursor.execute('''
            INSERT INTO clients(username, password, salt, hash_algo, iterations)
            VALUES(?, ?, ?, ?, ?)
            ''', (username, password, salt, hash_algo, iterations))
            CONN.commit()
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
        if CONN is not None:
            CONN.close()


def confirm_login(username: str, password_plaintext: str) -> bool | None:
    """
    This function confirms the login of a user
    :param username: username the user entered
    :param password_plaintext: password the user entered
    :return:True/False, None if an error occurred
    """
    global CONN
    try:
        cursor = CONN.cursor()
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
        if CONN is not None:
            CONN.close()


def create_chatroom(username: str, chat_name: str, settings: dict) -> bool | None:
    """
    This functions adds a chatroom id to the database. This will be referenced for client-to-chatroom connections throughout the program.
    :param settings: {login_required: bool,
    :param username: Username of the owner of the chatroom
    :param chat_name: Name of the chatroom
    :return: True/False, None if an error occurred
    """
    global CONN
    try:
        cursor = CONN.cursor()
        if not exists("chatrooms", chat_name):
            cursor.execute('''
                INSERT INTO chatrooms(chat_name, owner_id)
                VALUES(?, ?)''', (chat_name, username))
            return True
        else:
            print("Already exists")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return None


def join_chatroom(chat_name: str, username: str, password: Optional[str] = None, join_code: Optional[str] = None) -> bool | None:
    if exists("chatrooms", chat_name):
        return True
    if password:
        ...
    if join_code:
        ...
