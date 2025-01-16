import socket
import threading

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5213

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_IP, SERVER_PORT))
print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")

clients = {}  #username:socket
chats = {}  #chatid:[users]

def handle_client(client_socket):
    client_socket.send(b"Welcome to the chat server. Type your username and press enter to join the chat.\n")
    username = client_socket.recv(1024).decode().strip()
    clients[username] = client_socket
    print(f"{username} has connected.")

    while True:
        client_socket.send(b"Connect to general chat (G), join a chat (J), or create a new chat (C)?\n")
        choice = client_socket.recv(1024).decode().strip().lower()
        if choice.startswith(("g","j","c")):
            break
        else:
            client_socket.send(b"Invalid choice. Please enter G, J, or C to choose an option.\n")

    if choice == "g":
        chatid = "general"
        if chatid not in chats:
            chats[chatid] = [username]
    elif choice == "j":
        client_socket.send(b"Enter the chat ID of the chat you want to join:\n")
        chatid = client_socket.recv(1024).decode().strip()
        if chatid not in chats:
            client_socket.send(b"Invalid chat ID. Please enter a valid chat ID.\n")
    elif choice == "c":
        client_socket.send(b"Enter the name of the new chat:\n")
        chatid = client_socket.recv(1024).decode().strip()
        if chatid in chats:
            client_socket.send(b"Invalid Chat ID. Please enter a different chat ID.\n")
        else:
            chats[chatid] = [username]

    chats[chatid].append(username)
    print(f"{username} has joined the chat {chatid}.")
    clients[username].send(f"You have joined the chat {chatid}.\n".encode())

    while True:
        try:
            message = client_socket.recv(1024).decode().strip()
            for user in chats[chatid]:
                if user == username:
                    continue
                clients[user].send(f"{username}: {message}\n".encode())
        except:
            del clients[username]
            if chatid in chats:
                if username in chats[chatid]:
                    chats[chatid].remove(username)
                if len(chats[chatid]) == 0:
                    del chats[chatid]
            print(f"{username} has disconnected.")
            break


def start():
    server.listen()
    while True:
        client_socket, client_address = server.accept()
        print(f"Accepted connection from {client_address}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    start()