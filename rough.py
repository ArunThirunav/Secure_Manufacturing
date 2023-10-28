import os
from zipfile import ZipFile


filepath = "/home/arun/Programming/Secure_Manufacturing/080N0403.bin"
signature_filepath = "/home/arun/Programming/Secure_Manufacturing/080N0403_signature"
cur_path = os.path.dirname(filepath)
filename = os.path.basename(filepath)
signature_filename = os.path.basename(signature_filepath)

with ZipFile(cur_path+"/"+filename.split(".")[0]+".akds", 'w') as zip_object:
   # Adding files that need to be zipped
      zip_object.write(filename)
      zip_object.write(signature_filename)

# Check to see if the zip file is created
if os.path.exists('cur_path+"/"+filename.split(".")[0]+".zip"'):
   print("ZIP file created")
else:
   print("ZIP file not created")