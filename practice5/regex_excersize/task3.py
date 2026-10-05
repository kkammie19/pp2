import re

txt = "kamilla_ongdassyn test_string Python"

x = re.findall(r"[a-z] + _ [a-z] +", txt)

print(x)