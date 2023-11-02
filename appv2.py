import os
import hashlib
import logging
import PySimpleGUI as sg
from cryptography.fernet import Fernet

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
key = "R6Tv4of5jSC9jHQDPqzrZCwDElE4xklHRb9knNs5DT4="
logging.basicConfig(level=logging.DEBUG)
CIPHER_KEY_LEN = 64

class Cryptography:
    def __init__(self, key):
        self.fernet = Fernet(key)

    def encrypt(self, data):
        return self.fernet.encrypt(data)
    
    def decrypt(self, data):
        return self.fernet.decrypt(data)

def sign_button_handler(filename)->None:
    """
    Encrypts the contents of a file using a Fernet key and creates a new encrypted file with the extension ".cro".
    Calculates the SHA256 hash of the input file and writes it to the encrypted file.
    Displays a popup message indicating whether the encrypted file was successfully created or not.

    Args:
        filename (str): The path of the file to be encrypted.

    Returns:
        None
    """
    logging.debug("Enc_File_Location: %s", filename)
    enc_path = os.path.dirname(filename)
    enc_filename = os.path.join(enc_path, (os.path.basename(filename)).split(".")[0] + ".cro")
    
    try:
        with open(filename,"rb") as raw_file:
            bytes = raw_file.read()
        hash_bytes = hashlib.sha256(bytes).hexdigest()

        encryptor = Cryptography(key)
        encrypted = encryptor.encrypt(bytes)

        with open(enc_filename, 'wb') as encrypted_file:
            try:
                encrypted_file.write(bytearray(hash_bytes, 'utf-8'))
                encrypted_file.write(encrypted)
                sg.popup_ok("Encrypted File Created")
            except :
                sg.popup_error("Failed to Create Encrypted File")
    except FileNotFoundError:
        sg.popup_error("File Not Found. ")
    except FileExistsError:
        sg.popup_error("File Already Exists. ")
def verify_button_handler(file_name: str) -> None:
    """
    Verify the integrity of a file.

    Args:
        file_name (str): The name of the file to be verified.

    Returns:
        None: The function does not return any value. It only displays messages indicating the result of the file verification process.
    """

    ext = (os.path.basename(file_name)).split(".")[1]
    if ext == "cro": 
        try:
            with open(file_name, 'rb') as enc_file:
                cipher_text = enc_file.read()
            hash_bytes = cipher_text[0:CIPHER_KEY_LEN]
            decryptor = Cryptography(key)
            decrypted = decryptor.decrypt(cipher_text[CIPHER_KEY_LEN:])
            calculated_hashbytes =  hashlib.sha256(decrypted).hexdigest()

            if bytes(calculated_hashbytes, 'utf-8') == hash_bytes:
                sg.popup_ok("File Verification Success")
            else:
                sg.popup_error("File Corrupted")
        except (FileExistsError, FileNotFoundError):
            sg.popup_error("Cannot Verify the File")
    else:
        sg.popup_error("Invalid File Format")

if __name__ == "__main__":
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "Sign":
            sign_button_handler(values['sign_lineEdit'])
        if event == "Verify":
            verify_button_handler(values['verify_lineEdit'])

window.close()

