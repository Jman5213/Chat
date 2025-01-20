import socket
import threading

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5213

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, SERVER_PORT))
print(f"Connected to {SERVER_IP}:{SERVER_PORT}")


def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            if message == "quit":
                client.close()
                break
            else:
                print("\b\b"+message, end="")
        except:
            client.close()
            break


thread = threading.Thread(target=receive)
thread.start()

while True:
    message = f"{input("> ")}"
    print(message)
    if message == "/quit":
        break
    client.send(message.encode())

client.close()
