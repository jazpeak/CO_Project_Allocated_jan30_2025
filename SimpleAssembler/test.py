import re

s="ble r1,r2,rdhi"
print(re.split(pattern=r"[: ,]", string=s))

