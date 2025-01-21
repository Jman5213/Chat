import socket

import PySimpleGUI as sg

import Layouts

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5213
USERNAME = ''
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
window = sg.Window('Chat', layout=Layouts.layout_one_base)


def logout():
    client.send(f'LGT {USERNAME}'.encode())
    client.recv(1024).decode()
    exit()


def connect_to_server(password):
    client.connect((SERVER_IP, SERVER_PORT))
    print(f"Connected to {SERVER_IP}:{SERVER_PORT}")
    request_login(USERNAME, password)


def request_login(username, password):
    # later, like, actually request this from the server
    client.send(f'LGN {username} {password}'.encode())
    return client.recv(1024).decode()


def login_process():
    window['-STARTFRAME-'].update(visible=False)
    window['-LOGINFRAME-'].update(visible=True)
    attempts = 0
    while attempts < 3:
        attempts += 1
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            logout()
        elif event == '-USERNAME-' or event == '-PASSWORD-':
            if window['-USERNAME-'].values != '' and window['-PASSWORD-'].values != '':
                window['-OK-'].update(disabled=False)
            else:
                window['-OK-'].update(disabled=True)
        elif event == '-OK-':
            login = request_login(window['-USERNAME-'].values, window['-PASSWORD-'].values)  # True/False


def create_account():
    pass


def load_main_page():
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            logout()
        elif event == '-LOGIN-':
            login_process()
            break
        elif event == '-CREATEUSER-':
            create_account()
            break
            else:
            window['-CREATEFRAME-'].update(visible=False)
            window['-STARTFRAME-'].update(visible=True)


load_main_page()

"""
commands:
MSG <username> <chatid> <time/date> <message>       (message)
    MSGSENT
LGN <username> <password>                           (login)
    SUCCESS/FAILURE
CTU <username> <password>                          (create user)
    CREATED
CTC <username> <chatsettings>                       (create chat)
    CREATED
DLU <username> <password>                           (delete user)
    DELETED
DLC <username> <password>                           (delete chat)
    DELETED
JCH <username> <chatid>                             (join chat)
    CHTJOIN
LCH <username> <chatid>                             (leave chat)
    CHTLEFT
LGT <username>                                      (logout)
    ULOGOUT
"""
