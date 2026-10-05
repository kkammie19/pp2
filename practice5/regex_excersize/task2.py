import re 
txt ="abb"
x = re.match(r"ab{2, 3}", txt)
print(x.group())
