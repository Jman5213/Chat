import hashlib
import socket
import threading
import os
import database as db
import base64
from typing import Tuple

from database import confirm_login

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5213

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_IP, SERVER_PORT))
print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")

clients = {}  #username:socket



def save_chat(chatid: str, username: str, time: str, message: str):
    ...


def handle_message(client_socket, username: str, chatid: str, time: str, message: str):
    for user in chatid:
        if user != username:
            client_socket.send(f"{username}(Time:{time}:{message}".encode("utf-8"))



def login(client_socket,username: str, password: str):
    if confirm_login(username, password) is True:
        client_socket.send("Logged in".encode("utf-8"))
        return True
    elif confirm_login(username, password) is None:
        client_socket.send("An error occurred. Please try again.".encode("utf-8"))
        return None
    else:
        client_socket.send("Invalid username or password.".encode("utf-8"))
        return False


def create_user(client_socket, username: str, password: str):
    if not db.exists("clients", username):
        if db.add_user(username, password):
            client_socket.send("Created!".encode("utf-8"))
            return True
        else:
            client_socket.send("Unsuccessful".encode("utf-8"))
            return False
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
            commands[command](client_socket, *args)
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