file_path = input("Enter file path: ")

with open(file_path, "r", encoding="utf-8") as file:
    lines = file.readlines()

print("Number of lines:", len(lines))