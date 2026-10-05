import re

txt = "Python regex Practice"

x = re.findall(r"[A-z][a-z] + ", txt)

print(x)