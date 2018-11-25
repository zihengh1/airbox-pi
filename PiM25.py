import time
import pigpio
import commands
from datetime import datetime

def bytes2hex(s):
    return "".join("{:02x}".format(c) for c in s)

def data_read(dstr):
    # data standard style
    standard = "424d001c"
    data_len = 64
    weather = ""
    # print(dstr)
    index = dstr.find(standard)
    if(index == -1 or len(dstr) < 64):
        return weather
    else:
        data_slice = dstr[index : index + data_len]
        weather += '|PM1_0:%d' % (int(data_slice[16] + data_slice[17] + data_slice[18] + data_slice[19], 16))       # pm1
        weather += '|PM2_5:%d' % (int(data_slice[20] + data_slice[21] + data_slice[22] + data_slice[23], 16))       # pm25
        weather += '|PM_10:%d' % (int(data_slice[24] + data_slice[25] + data_slice[26] + data_slice[27], 16))       # pm10
        weather += '|Tmp:%d' % (int(data_slice[48] + data_slice[49] + data_slice[50] + data_slice[51], 16) / 10)    # Temperature
        weather += '|RH:%d' % (int(data_slice[52] + data_slice[53] + data_slice[54] + data_slice[55], 16) / 10)     # Humidity 
        return weather 

RX = 15
path = "/home/pi/Data/"
status, process = commands.getstatusoutput('sudo pidof pigpiod')

if status:  #  it wasn't running, so start it
    print "pigpiod was not running"
    commands.getstatusoutput('sudo pigpiod')  # start it
    time.sleep(1)
    pi = pigpio.pi()

if not status:  # if it worked, i.e. if it's running...
    pigpiod_process = process
    print "pigpiod is running, process ID is: ", pigpiod_process
    try:
        pi = pigpio.pi()  # local GPIO only
        print "pi is instantiated successfully"
    except Exception as e:
        print "problem instantiating pi, the exception message is: ", e

pi.set_mode(RX, pigpio.INPUT)
try:
    pi.bb_serial_read_close(RX)
except Exception as e:
    pass

while True:
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S").split(" ")
    weather_data = ""
    try:
        pi.bb_serial_read_open(RX, 9600)
        time.sleep(0.9)
        (status, data) = pi.bb_serial_read(RX)
        if status:
            print("read_something")
            data_hex = bytes2hex(data)
            weather_data = data_read(data_hex) 
            if len(weather_data):
                weather_data += '|%s_%s' % (str(now_time[0]), str(now_time[1]))
                print(weather_data)
        else:
            print("read_nothing")
       
    except Exception as e:
        print("close")
        pi.bb_serial_read_close(RX)
        print("close success")

    with open(path + str(now_time[0]) + ".txt", "a") as f:
        try:
            if len(weather_data):
                f.write(weather_data + "\n")
        except Exception as e:
            print(e)
            print "Error: writing to SD"    
    pi.bb_serial_read_close(RX)
    time.sleep(295)

pi.stop()
print("End")
   
