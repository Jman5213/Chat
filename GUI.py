import socket

import PySimpleGUI as sg

layout = []
SERVER_IP = "127.0.0.1"
SERVER_PORT = 5213
USERNAME = ''
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def logout():
    client.send(f'LGT {USERNAME}'.encode())
    client.recv(1024).decode()
    exit()


def connect_to_server():
    client.connect((SERVER_IP, SERVER_PORT))
    print(f"Connected to {SERVER_IP}:{SERVER_PORT}")


def request_login(username, password):
    # later, like, actually request this from the server
    return True


def login_process():
    start_frame = [
        [sg.Push(), sg.Button('Login', key='-LOGIN-'), sg.Button('Create Account', key='-CREATEUSR-'), sg.Push()]
    ]

    create_account_frame = [
        [sg.Push(), sg.Text("Please enter your information"), sg.Push()],
        [sg.Push(), sg.Text('Invalid Username', colors='red', key='-ERROR-', visible=False), sg.Push()],
        [sg.Push(), sg.Text("Username:"), sg.InputText(key='-USERNAME-', do_not_clear=True), sg.Push()],
        [sg.Push(), sg.Text("Password:"), sg.InputText(key='-PASSWORD-', password_char='*', do_not_clear=True),
         sg.Push()],
        [sg.Push(), sg.Button('Create Account'), sg.Button('Cancel'), sg.Push()]
    ]

    login_frame = [
        [sg.Push(), sg.Text("Incorrect Username/Password combination", colors='red', key='-ERROR-', visible=False),
         sg.Push()],
        [sg.Push(), sg.Text("Username:"), sg.InputText(key='-USERNAME-', do_not_clear=True, enable_events=True), sg.Push()],
        [sg.Push(), sg.Text("Password:"), sg.InputText(key='-PASSWORD-', password_char='*', enable_events=True),
         sg.Push()],
        [sg.Button('Ok', disabled=True, key='-OK-'), sg.Button('Cancel')]
    ]
    layout = [
        [sg.Push(), sg.Text("Welcome to the Chat app"), sg.Push()],
        start_frame
    ]

    window = sg.Window('Chat App', layout)

    attempts = 0

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            exit()
        if event == '-PASSWORD-' or event == '-USERNAME-':
            if values['-USERNAME-'] != '' and values['-PASSWORD-'] != '':
                window['-OK-'].update(disabled=False)
            else:
                window['-OK-'].update(disabled=True)

        if event == '-OK-':
            login = request_login(values['-USERNAME-'], values['-PASSWORD-'])
            if not login:
                window['-ERROR-'].update(visible=True)
                window['-OK-'].update(disabled=True)
                window['-PASSWORD-'].update(value='')
                attempts += 1
                if attempts == 3:
                    exit()
            else:
                window.close()
                return


def load_main_page():
    layout = [
        [sg.Menu([['Profile'], ['Friends'], ['Chats'], ['Settings']])],
        [sg.Push(), sg.Text("Welcome to the Chat app"), sg.Push()],
        [sg.Column([
            [sg.Text("Friends Online:")],
            [sg.Listbox(values=[], size=(20, 6), enable_events=True, key='-FRIENDS-')]
        ]), sg.Column([
            [sg.Text("Chats:")],
            [sg.Listbox(values=[], size=(20, 6), enable_events=True, key='-CHATS-')]
        ])]
    ]

    window = sg.Window('Chat App', layout)
    connect_to_server()

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Quit'):
            logout()


login_process()
load_main_page()

"""
commands:
MSG <username> <chatid> <time/date> <message>  (message)
    MSGSENT
LGN <username> <password>                      (login)
    SUCCESS/FAILURE
CTU <username> <password> <fname> <lname>      (create user)
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
