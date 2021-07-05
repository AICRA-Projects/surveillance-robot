import time
from smbus import SMBus
addr = 0x8
bus = SMBus(1)
numb = True
print("state")
for i in range(0,100):
    bus.write_byte(addr, i)