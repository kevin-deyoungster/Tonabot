import re

term = r"([0-9]+){1,3}\s?gb"
string = "Brand new iPhone 8 Plus 256gb "
m = re.findall(term,string.lower())
if m:
    print(m)
else:
    print("Nada")