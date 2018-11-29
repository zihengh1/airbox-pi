import time
import pigpio
import commands
from datetime import datetime
import PiM25_config as Conf
import os

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
        print(data_slice)
        weather += '|CFPM1.0=%d' % (int(data_slice[8] + data_slice[9] + data_slice[10] + data_slice[11], 16))        # cf_pm1 
        weather += '|CFPM2.5=%d' % (int(data_slice[12] + data_slice[13] + data_slice[14] + data_slice[15], 16))      # cf_pm2.5
        weather += '|CFPM10=%d' % (int(data_slice[16] + data_slice[17] + data_slice[18] + data_slice[19], 16))     # cf_pm10
        weather += '|s_d2=%d' % (int(data_slice[20] + data_slice[21] + data_slice[22] + data_slice[23], 16))       # pm1
        weather += '|s_d0=%d' % (int(data_slice[24] + data_slice[25] + data_slice[26] + data_slice[27], 16))       # pm2.5
        weather += '|s_d1=%d' % (int(data_slice[28] + data_slice[29] + data_slice[30] + data_slice[31], 16))       # pm10
        weather += '|s_t0=%d' % (int(data_slice[48] + data_slice[49] + data_slice[50] + data_slice[51], 16) / 10)    # Temperature
        weather += '|s_h0=%d' % (int(data_slice[52] + data_slice[53] + data_slice[54] + data_slice[55], 16) / 10)     # Humidity 
        return weather 

def upload_data(msg):
    msg += '|app=%s' % (Conf.APP_ID)
    msg += '|device=%s' % (Conf.DEVICE)
    msg += '|device_id=%s' % (Conf.DEVICE_ID)
    msg += '|gps_lat=%s' % (Conf.GPS_LAT)
    msg += '|gps_lon=%s' % (Conf.GPS_LON)
    msg += Conf.others
    
    Restful_URL = Conf.Restful_URL
    print(msg)
    restful_str = "wget -O /tmp/last_upload.log \"" + Restful_URL + "?device_id=" + Conf.DEVICE_ID + "&msg=" + msg + "\""
    os.system(restful_str)
    
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

while True:
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S").split(" ")
    weather_data = ""
    try:
        pi.bb_serial_read_close(RX)
    except Exception as e:
        pass
    try:
        pi.bb_serial_read_open(RX, 9600)
        time.sleep(0.9)
        (status, data) = pi.bb_serial_read(RX)
        if status:
            print("read_something")
            data_hex = bytes2hex(data)
            weather_data = data_read(data_hex) 
            if len(weather_data):
                weather_data += '|date=%s' % (str(now_time[0]))
                weather_data += '|time=%s' % (str(now_time[1]))
                upload_data(weather_data)
        else:
            print("read nothing")
 
    except Exception as e:
        print(e)
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
    time.sleep(5)

pi.stop()
print("End")

