import re 

txt = "Practice lesson 5"

replace = re.sub(r" ", "9", txt)

print(replace)