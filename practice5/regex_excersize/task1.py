import re
txt = "ababbb"
x = re.match(r"ab*", txt)
print(x.group())