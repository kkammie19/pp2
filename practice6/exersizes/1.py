#List directories, files, and everything in a specified path
import os

path = input("Enter path: ")

for item in os.listdir(path):
    full_path = os.path.join(path, item)

    if os.path.isdir(full_path):
        print(item)


#to list only files 
import os

path = input("Enter path: ")

for item in os.listdir(path):
    full_path = os.path.join(path, item)

    if os.path.isfile(full_path):
        print(item)


#to list all files and directors 
import os

path = input("Enter path: ")

print(os.listdir(path))        