import PySimpleGUI as sg


layout = []

def login_process():
    login_frame = [
        [sg.Push(), sg.Text("Incorrect Username/Password combination", colors='red', key='-ERROR-', visible=False),
         sg.Push()],
        [sg.Push(), sg.Text("Username:"), sg.InputText(key='-USERNAME-', do_not_clear=True, enable_events=True), sg.Push()],
        [sg.Push(), sg.Text("Password:"), sg.InputText(key='-PASSWORD-', password_char='*', enable_events=True),
         sg.Push()]
    ]
    layout = [
        [sg.Push(), sg.Text("Welcome to the Chat app"), sg.Push()],
        [sg.Frame("Login", login_frame)],
        [sg.Button('Ok', disabled=True, key='-LOGIN-'), sg.Button('Cancel')]
    ]

    window = sg.Window('Chat App', layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            exit()
        if event == '-PASSWORD-' or event == '-USERNAME-':
            if values['-USERNAME-'] != '' and values['-PASSWORD-'] != '':
                window['-LOGIN-'].update(disabled=False)
            else:
                window['-LOGIN-'].update(disabled=True)

        if event == '-LOGIN-':
            login = request_login(values['-USERNAME-'], values['-PASSWORD-'])
            if not login:
                window['-ERROR-'].update(visible=True)
                window['-LOGIN-'].update(disabled=True)
                window['-PASSWORD-'].update(value='')
            else:
                return


def load_main_page():
    layout = [
        [sg.Menu([['Profile'], ['Friends'], ['Chats']])],
        [sg.Push(), sg.Text("Welcome to the Chat app"), sg.Push()],
        [sg.Column([
            [sg.Text("Friends Online:")],
            [sg.Listbox(values=[], size=(20, 6), enable_events=True, key='-FRIENDS-')]
        ])],
        [sg.Column([
            [sg.Text("Chats:")],
            [sg.Listbox(values=[], size=(20, 6), enable_events=True, key='-CHATS-')]
        ])]
    ]
    window = sg.Window('Chat App', layout)
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Quit'):
            exit()

login_process()
load_main_page()
