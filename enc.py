import PySimpleGUI as sg
import sys
import os
import hashlib
from zipfile import ZipFile
import time
# import required module
from cryptography.fernet import Fernet


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

def calculateEnc(filename)->None:
    # using the generated key
    key = "R6Tv4of5jSC9jHQDPqzrZCwDElE4xklHrb9knNS5DT4="
    fernet = Fernet(key)
    with open(filename,"rb") as f:
        bytes = f.read()
        print("Len: ", len(bytes))
        
    # encrypting the file
    encrypted = fernet.encrypt(bytes)
    
    # opening the file in write mode and 
    # writing the encrypted data
    with open('encry.cro', 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
    
    decrypted = fernet.decrypt(encrypted)
    with open('decry.bin', 'wb') as encrypted_file:
        encrypted_file.write(decrypted)
        
if __name__ == "__main__":
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "Sign":
            calculateEnc(values["sign_lineEdit"])

window.close()