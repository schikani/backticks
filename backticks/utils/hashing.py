import hashlib

# BUF_SIZE = 32768 # Read file in 32kb chunks
BUF_SIZE = 1024


def sha1_hashing(filename):
   """"This function returns the SHA-1 hash
   of the file passed into it"""

   # make a hash object
   h = hashlib.sha1()

   # open file for reading in binary mode
   with open(filename,'rb') as file:

       # loop till the end of the file
       chunk = 0
       while chunk != b'':
           # read only 1024 bytes at a time
           chunk = file.read(BUF_SIZE)
           h.update(chunk)

   # return the hex representation of digest
   return h.hexdigest()

