import PySimpleGUI as sg
import sys
import hashlib

sg.theme('TealMono')
t1=sg.Input("", key='sign_lineEdit')
l1 = sg.FileBrowse("Firmware File")
b1 = sg.Button("Sign")
tab1=[[t1,l1], [b1]]

t2=sg.Input("", key='verify_lineEdit')
f2 = sg.FileBrowse("Veification File")
b2 = sg.Button("Verify")
b3 = sg.Button("Verify&Flash")
tab2=[[t2, f2], [b2, b3]]

layout = [[sg.TabGroup([
   [sg.Tab('Signature', tab1),
   sg.Tab('Verify and Flash', tab2)]])]
]
window = sg.Window('Danfoss Secure Manufacturing Tool', layout)
previous_filename = ""


def calculateHash(filename):
    with open(filename,"rb") as f:
        bytes = f.read()
        return hashlib.sha256(bytes).hexdigest()
    
def createSignatureFile(fileName):
    hashValue = calculateHash(fileName)
    with open(fileName.split(".")[0]+"_signature", "w") as f:
        f.write(hashValue)
        return True

def verifySignatureFile(fileName):
    with open(fileName.split(".")[0]+"_signature", "r") as f:
        bytes = f.read()
        if calculateHash(fileName) == bytes:
            return True
        else:
            return False

def signButtonHandler():
    if previous_filename != values["sign_lineEdit"]:
        previous_filename = values["sign_lineEdit"]
        if createSignatureFile(values["sign_lineEdit"]):
            sg.popup_auto_close("Signature File Created")
        else:
            sg.popup_error("Cannot Create Signature File")
    else:
        print("Enter Proper Firmware File")

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
        break
    if event == "Sign":
        signButtonHandler()
    if event == "Verify":
        pass

window.close()