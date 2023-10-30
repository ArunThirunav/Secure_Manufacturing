import PySimpleGUI as sg
import sys
import os
import hashlib
from cryptography.fernet import Fernet
from zipfile import ZipFile
import time

sg.theme('Reddit')
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
key = "R6Tv4of5jSC9jHQDPqzrZCwDElE4xklHRb9knNs5DT4="
fernet = Fernet(key)
CIPHER_KEY_LEN = 64

def signButtonHandler(filename)->None:
    global previous_filename
    enc_filename = (os.path.basename(filename)).split(".")[0] + ".cro"
    try:
        with open(filename,"rb") as f:
            bytes = f.read()
        hash_bytes = hashlib.sha256(bytes).hexdigest()
        encrypted = fernet.encrypt(bytes)
        with open(enc_filename, 'wb') as encrypted_file:
            try:
                encrypted_file.write(bytearray(hash_bytes, 'utf-8'))
                encrypted_file.write(encrypted)
                sg.popup_ok("Encrypted File Created")
            except:
                sg.popup_error("Failed to Create Encrypted File")
    except FileNotFoundError or FileExistsError:
        sg.popup_error("File Not Found. ")

def verifyButtonHandler(file_name)->None:
    ext = (os.path.basename(file_name)).split(".")[1]
    if ext == "cro": 
        try:
            with open(file_name, 'rb') as f:
                cipher_text = f.read()
            hash_bytes = cipher_text[0:CIPHER_KEY_LEN]
            decrypted = fernet.decrypt(cipher_text[CIPHER_KEY_LEN:])
            calculated_hashbytes =  hashlib.sha256(decrypted).hexdigest()
            
            if bytes(calculated_hashbytes, 'utf-8') == hash_bytes:
                sg.popup_ok("File Verification Success")
            else:
                sg.popup_error("File Corrupted")
        except:
            sg.popup_error("Cannot Verify the File")
    else:
        sg.popup_error("Invalid File Format")

if __name__ == "__main__":
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "Sign":
            signButtonHandler(values['sign_lineEdit'])
        if event == "Verify":
            verifyButtonHandler(values['verify_lineEdit'])

window.close()

