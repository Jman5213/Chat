import hashlib
import socket
import threading
import os
import database as db
import base64
from opcode import haslocal

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5213

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_IP, SERVER_PORT))
print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")

clients = {}  #username:socket
chats = {}  #chat_id:[users]


def generate_salt():
    # 128 bit salt value
    salt = os.urandom(16)
    return salt


def hash_password(password: str):
    salt = generate_salt()
    iterations = 100_000
    hash_value = hashlib.pbkdf2_hmac(
        "sha512",
        password.encode("utf-8"),
        salt,
        iterations
    )
    password_hash = salt + hash_value
    password_hash = base64.b64encode(password_hash).decode("utf-8")
    return_value = p
    return

def save_chat():
    ...


def handle_message(client_socket, username: str, chatid: str, time: str, message: str):
    for user in chatid:
        if user != username:
            client_socket.send(f"{username}(Time:{time}:{message}".encode("utf-8"))



def login(username: str, password: str):
    return True


def create_user(client_socket, username: str, password: str):
    if not clients[username]:
        hashed_password = hash_password(password)
        salt, clients[username] = hashed_password[:16], hashed_password[16:]
        client_socket.send("Created".encode("utf-8"))
        db.add_user(username, clients[username], salt, )
        return True
    else:
        client_socket.send("Username already exits".encode("utf-8"))
        return False


def create_chat(username: str, settings: dict):
    ...


def delete_user(username: str, password: str):
    ...


def delete_chat(username: str, password: str, chatid: str):
    ...


def join_chat(username: str, chatid: str):
    ...


def leave_chat(username: str, chatid: str):
    ...


def logout(username: str):
    ...


def handle_client(client_socket):
    while True:
        message = client_socket.recv(1024).decode()
        try:
            command, *args = message.split()
            commands[command](*args)
        except:
            client_socket.close()
            break


def start():
    server.listen()
    while True:
        client_socket, client_address = server.accept()
        print(f"Accepted connection from {client_address}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    """
    commands:
    MSG <username> <chatid> <time/date> <message>  (message)
        MSGSENT
    LGN <username> <password>                      (login)
        SUCCESS/FAILURE
    CTU <username> <password>                      (create user)
        CREATED
    CTC <username> <chatsettings>                  (create chat)
        CREATED
    DLU <username> <password>                      (delete user)
        DELETED
    DLC <username> <password>                      (delete chat)
        DELETED
    JCH <username> <chatid>                        (join chat)
        CHTJOIN
    LCH <username> <chatid>                        (leave chat)
        CHTLEFT
    LGT <username>                                 (logout)
        ULOGOUT
    """

    commands = {
        "MSG": handle_message,
        "LGN": login,
        "CTU": create_user,
        "CTC": create_chat,
        "DLU": delete_user,
        "DLC": delete_chat,
        "JCH": join_chat,
        "LCH": leave_chat,
        "LGT": logout
    }
    db.init_db()
    start()