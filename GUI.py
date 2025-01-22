import socket

import PySimpleGUI as sg

import Layouts

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5213
USERNAME = ''
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
window = sg.Window('Chat', layout=Layouts.layout_one_base)


def logout():
    try:
        client.send(f'LGT {USERNAME}'.encode())
        client.recv(1024).decode()
    except:
        pass
    finally:
        exit()


def connect_to_server(password):
    client.connect((SERVER_IP, SERVER_PORT))
    print(f"Connected to {SERVER_IP}:{SERVER_PORT}")
    request_login(USERNAME, password)


def request_login(username, password):
    # later, like, actually request this from the server
    client.send(f'LGN {username} {password}'.encode())
    return client.recv(1024).decode()


def request_create(username, password):
    client.send(f'CTU {username} {password}'.encode())
    return client.recv(1024).decode()


def user_available(username):
    pass


def login_process():
    global USERNAME

    window['-STARTFRAME-'].update(visible=False)
    window['-LOGINFRAME-'].update(visible=True)
    attempts = 0
    while attempts < 3:
        attempts += 1
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            logout()
        if event == '-LGNCANCEL-':
            window['-STARTFRAME-'].update(visible=True)
            window['-CREATEFRAME-'].update(visible=False)
            window['-LOGINFRAME-'].update(visible=False)
            return
        if event == '-LGNUSERNAME-' or event == '-LGNPASSWORD-':
            if values['-LGNUSERNAME-'] != '' and values['-LGNPASSWORD-'] != '':
                window['-OK-'].update(disabled=False)
            else:
                window['-OK-'].update(disabled=True)
        if event == '-OK-':
            login = request_login(values['-LGNUSERNAME-'], values['-LGNPASSWORD-'])  # True/False
            if login:
                USERNAME = values['-LGNUSERNAME-']
                load_main_page()


def create_account():
    window['-STARTFRAME-'].update(visible=False)
    window['-CREATEFRAME-'].update(visible=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            logout()
        if event == '-CRTCANCEL-':
            window['-STARTFRAME-'].update(visible=True)
            window['-CREATEFRAME-'].update(visible=False)
            window['-LOGINFRAME-'].update(visible=False)
            return
        if event == '-CRTUSERNAME-' or event == '-CRTPASSWORD-' or event == '-CONFPASSWORD-':
            if values['-CRTUSERNAME-'] != '' and values['-CRTPASSWORD-'] != '' and values['-CONFPASSWORD-'] != '':
                if values['-CRTPASSWORD-'] != values['-CONFPASSWORD-']:
                    window['-OK-'].update(disabled=True)
                    window['-PASSERROR-'].update(visible=True)
                    window['-ERROR-'].update(visible=False)
                    window['-SERVERROR-'].update(visible=False)
                    window['-CREATE-'].update(disabled=True)
                elif not user_available(values['-CRTUSERNAME-']):
                    window['-OK-'].update(disabled=True)
                    window['-ERROR-'].update(visible=True)
                    window['-PASSERROR-'].update(visible=False)
                    window['-SERVERROR-'].update(visible=False)
                    window['-CREATE-'].update(disabled=True)
                else:
                    window['-CREATE-'].update(disabled=True)
        if event == '-OK-':
            if request_create(values['-CRTUSERNAME-'], values['-CRTPASSWORD-']):
                load_main_page()
            else:
                window['-OK-'].update(disabled=True)
                window['-SERVERROR-'].update(visible=True)



def load_main_page():
    pass


def load_start_page():
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            logout()
        elif event == '-LOGIN-':
            login_process()
        elif event == '-CREATEUSER-':
            create_account()
        else:
            window['-STARTFRAME-'].update(visible=True)
            window['-CREATEFRAME-'].update(visible=False)
            window['-LOGINFRAME-'].update(visible=False)


load_start_page()

"""
commands:
MSG <username> <chatid> <time/date> <message>       (message)
    MSGSENT
LGN <username> <password>                           (login)
    SUCCESS/FAILURE
CTU <username> <password>                           (create user)
    CREATED
UAV <username>                                      (username available)
    TRUE/FALSE
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
