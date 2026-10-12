import os

path = input("Enter file path: ")

if os.path.exists(path):
    if os.path.isfile(path) and os.access(path, os.W_OK):
        os.remove(path)
        print("File deleted successfully")
    else:
        print("Not a file or no write permission")
else:
    print("Path does not exist")