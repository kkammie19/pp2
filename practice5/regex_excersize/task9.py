import re

txt = "HelloWorldPython"

x = re.sub(r"(?=[A-Z])", " ", txt).strip()

print(x)