import hashlib
import sys


def calculateHash(filename):
    with open(filename,"rb") as f:
        bytes = f.read()
        return hashlib.sha256(bytes).hexdigest()
    
def createSignatureFile(fileName):
    hashValue = calculateHash(fileName)
    with open(fileName.split(".")[0]+"_signature", "w") as f:
        f.write(hashValue)

def verifySignatureFile(fileName):
    with open(fileName.split(".")[0]+"_signature", "r") as f:
        bytes = f.read()
        print(bytes)
        if calculateHash(fileName) == bytes:
            print("Valid")
        else:
            print("Invalid")

if __name__ == "__main__":
    fileName = sys.argv[1]
    # createSignatureFile(fileName)
    verifySignatureFile(fileName)