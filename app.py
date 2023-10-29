import PySimpleGUI as sg
import sys
import os
import hashlib
from zipfile import ZipFile

"""
"""

sg.theme('SystemDefault')
t1=sg.Input("", key='sign_lineEdit', readonly='True')
l1 = sg.FileBrowse("Firmware File")
b1 = sg.Button("Sign")
tab1=[[t1,l1], [b1]]

t2=sg.Input("", key='verify_lineEdit')
f2 = sg.FileBrowse("Verification File")
b2 = sg.Button("Verify")
b3 = sg.Button("Verify&Flash")
tab2=[[t2, f2], [b2, b3]]

layout = [[sg.TabGroup([
   [sg.Tab('Signature', tab1),
   sg.Tab('Verify & Flash', tab2)]])]
]
window = sg.Window('Danfoss Secure Manufacturing Tool', layout)
previous_filename = ""


def calculateHash(filename):
    with open(filename,"rb") as f:
        bytes = f.read()
        return hashlib.sha256(bytes).hexdigest()
    
def createSignatureFile(fileName):
    hashValue = calculateHash(fileName)
    with open(fileName.split(".")[0]+"_signature.txt", "w") as f:
        f.write(hashValue)
        return True

def verifySignatureFile(fileName):
    with open(fileName.split(".")[0]+"_signature.txt", "r") as f:
        bytes = f.read()
        if calculateHash(fileName) == bytes:
            return True
        else:
            return False

def signButtonHandler()->None:
    global previous_filename
    if previous_filename != values["sign_lineEdit"]:
        previous_filename = values["sign_lineEdit"]
        if createSignatureFile(previous_filename):
            if zipFileCreation(previous_filename):
                os.remove(previous_filename.split(".")[0]+"_signature.txt")
                sg.popup_ok("Signature File Created")
            else:
                sg.popup_error("Failed during package creation")
        else:
            sg.popup_error("Cannot Create Signature File")
    else:
        sg.popup_error("Same Signature File")


def verifyButtonHandler()->None:
    if verifySignatureFile(values["verify_lineEdit"]):
        sg.popup_notify("Valid FW File")
    else:
        sg.popup_error("Invalid FW File")


def zipFileCreation(cur_path):
    filename = os.path.basename(cur_path)
    zip_filename = filename.split(".")[0]
    signature_filename = zip_filename+"_signature.txt"
    cur_path = os.path.dirname(cur_path)

    with ZipFile(cur_path+"/"+zip_filename+".cro", 'w') as zip_object:
        try:
            zip_object.write(filename)
            zip_object.write(signature_filename)
            return True
        except FileNotFoundError:
            return False

# if new function need to be added add it in this function pointer
EVENT_INDEX = 0
FUNCTION_INDEX = 1

function_pointer = [
    ["Sign", signButtonHandler],
    ["Verify", verifyButtonHandler]
]

if __name__ == "__main__":
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        for i in function_pointer:
            if i[EVENT_INDEX] == event:
                i[FUNCTION_INDEX]()

window.close()

