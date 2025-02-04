import PySimpleGUI as sg

start_frame = [
    [sg.Push(), sg.Button('Login', key='-LOGIN-'), sg.Button('Create Account', key='-CREATEUSER-'), sg.Push()]
]

create_account_frame = [
    [sg.Push(), sg.Text("Please enter your information"), sg.Push()],
    [sg.Push(), sg.Text('Invalid Username', colors='red', key='-ERROR-', visible=False),
     sg.Text("Passwords do not match", colors="red", key='-PASSERROR-', visible=False),
     sg.Text("Server error, please try again", colors='red', key='-SERVERROR-', visible=False), sg.Push()],
    [sg.Push(), sg.Text("Username:"), sg.InputText(key='-CRTUSERNAME-', enable_events=True), sg.Push()],
    [sg.Push(), sg.Text("Password:"), sg.InputText(key='-CRTPASSWORD-', password_char='*', enable_events=True),
     sg.Push()],
    [sg.Push(), sg.Text("Confirm Password:"), sg.InputText(key='-CONFPASSWORD-', password_char='*', enable_events=True),
     sg.Push()],
    [sg.Push(), sg.Button('Create Account', key='-CREATE-', disabled=True), sg.Button('Cancel', key='-CRTCANCEL-'),
     sg.Push()]
]

login_frame = [
    [sg.Push(), sg.Text("Incorrect Username/Password combination", colors='red', key='-INVALID-', visible=False),
     sg.Text("Server Error", colors='red', key="-SERVERERROR-", visible=False),
     sg.Push()],
    [sg.Push(), sg.Text("Username:"), sg.InputText(key='-LGNUSERNAME-', do_not_clear=True, enable_events=True),
     sg.Push()],
    [sg.Push(), sg.Text("Password:"), sg.InputText(key='-LGNPASSWORD-', password_char='*', enable_events=True),
     sg.Push()],
    [sg.Button('Ok', disabled=True, key='-OK-'), sg.Button('Cancel', key='-LGNCANCEL-')]
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
