import re

txt = "abaaab abracadabra a123b"

x = re.match(r"a.*b$", txt)

print(x.qroup())