import PySimpleGUI as sg

sg.theme('TealMono')   # Add a touch of color
# All the stuff inside your window.
layout = [
    [[sg.Input(), sg.FileBrowse()]],
    [sg.Button("Sign"), sg.Button("Verify")]
]
# Create the Window
window = sg.Window('Secure Manufacturing', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break

    if values[0] == "" and event == "Sign":
        print("Enter Proper Firmware File")

window.close()