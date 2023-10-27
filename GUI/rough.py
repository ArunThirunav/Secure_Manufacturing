import PySimpleGUI as sg
sg.set_options(font=("Arial Bold",14))

t1=sg.Input("", key='-Sign-')
l1 = sg.FileBrowse("Firmware File")
b1 = sg.Button("Sign")
tab1=[[t1,l1], [b1]]

t2=sg.Input("", key='-Verify-')
f2 = sg.FileBrowse("Veification File")
b2 = sg.Button("Verify")
b3 = sg.Button("Verify&Flash")
tab2=[[t2, f2], [b2, b3]]

layout = [[sg.TabGroup([
   [sg.Tab('Signature', tab1),
   sg.Tab('Verify and Flash', tab2)]])]
]
window = sg.Window('Secure Manufacturing', layout)

while True:
   event, values = window.read()
   print (values['-Sign-'])
   if event in (sg.WIN_CLOSED, 'Exit'):
      break

window.close()