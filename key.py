from random import seed, randint
from time import time
seed(time)
num = hex(randint(10000000, 99999999) * 167)
num = num.strip("0x")
print(num)