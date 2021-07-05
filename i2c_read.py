import smbus
import time
bus = smbus.SMBus(1)
addr = 0x8
addr_rec = 0x9
def writenumber(val):
    bus.write_byte(addr,val)
    return -1

while True:
    try:
        data = bus.read_byte(addr_rec)
        print(data)
        if data == 90:
            in1 = 16
            writenumber(in1)
            time.sleep(0.05)
            in1 = 11
            writenumber(in1)
        elif data == 80:
            in1 = 15
            writenumber(in1)
        elif data == 70:
            in1 = 3
            writenumber(in1)
        elif data == 50:
            in1 = 10
            writenumber(in1)
        else:
            in1 = 0
            writenumber(in1)
    except OSError:
        data = bus.read_byte(addr_rec)
        print(data)
    except IOError:
        data = bus.read_byte(addr_rec)
        print(data)
        
        
        