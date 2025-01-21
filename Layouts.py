import PySimpleGUI as sg

start_frame = [
    [sg.Push(), sg.Button('Login', key='-LOGIN-'), sg.Button('Create Account', key='-CREATEUSER-'), sg.Push()]
]

create_account_frame = [
    [sg.Push(), sg.Text("Please enter your information"), sg.Push()],
    [sg.Push(), sg.Text('Invalid Username', colors='red', key='-ERROR-', visible=False), sg.Push()],
    [sg.Push(), sg.Text("Username:"), sg.InputText(key='-USERNAME-', do_not_clear=True), sg.Push()],
    [sg.Push(), sg.Text("Password:"), sg.InputText(key='-PASSWORD-', password_char='*', do_not_clear=True), sg.Push()],
    [sg.Push(), sg.Text("Confirm Password:"), sg.InputText(key='-CONFPASSWORD-', password_char='*', do_not_clear=True),
     sg.Push()],
    [sg.Push(), sg.Button('Create Account', key='-CREATE-'), sg.Button('Cancel', key='-CANCEL-'), sg.Push()]
]

login_frame = [
    [sg.Push(), sg.Text("Incorrect Username/Password combination", colors='red', key='-ERROR-', visible=False),
     sg.Push()],
    [sg.Push(), sg.Text("Username:"), sg.InputText(key='-USERNAME-', do_not_clear=True, enable_events=True), sg.Push()],
    [sg.Push(), sg.Text("Password:"), sg.InputText(key='-PASSWORD-', password_char='*', enable_events=True),
     sg.Push()],
    [sg.Button('Ok', disabled=True, key='-OK-'), sg.Button('Cancel', key='-CANCEL-')]
]

layout_one_base = [
    [sg.Push(), sg.Text("Welcome to the Chat app"), sg.Push()],
    [sg.Column(start_frame, key='-STARTFRAME-'), sg.Column(create_account_frame, visible=False, key='-CREATEFRAME-'),
     sg.Column(login_frame, visible=False, key='-LOGINFRAME-')],
]

home_page_frame = [
    [sg.Column([
        [sg.Text("Friends Online:")],
        [sg.Listbox(values=[], size=(20, 6), enable_events=True, key='-FRIENDS-')]
    ]), sg.Column([
        [sg.Text("Chats:")],
        [sg.Listbox(values=[], size=(20, 6), enable_events=True, key='-CHATS-')]
    ])]
]

home_page_base = [
    [sg.Menu([['Profile'], ['Friends'], ['Chats'], ['Settings']])],
    [sg.Push(), sg.Text("Welcome to the Chat app"), sg.Push()],
    [sg.Column(home_page_frame, key='-HOMEFRAME-')]
]
