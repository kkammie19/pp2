import re

txt = "KamillaOngdassynKbtu"

x = re.split(r"(?[A-Z])", txt)

print(x)