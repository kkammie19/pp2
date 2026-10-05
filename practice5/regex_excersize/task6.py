import re

txt = "Hello, world. Practice lesson"

x = re.sub(r"[ ,.]", ":", txt)

print(x)