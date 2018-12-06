import time
import pigpio
import commands
from datetime import datetime
import PiM25_config as Conf
import os
import re

def dms2dd(degree, minutes, seconds, direction):
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60);
    if direction == 'S' or direction == 'W':
        dd *= -1
    return round(dd, 6);

def dmm2dd(dir, DMM):
    DMM = str(abs(float(DMM)))
    index = DMM.find(".")
    D = int(DMM[:index-2])
    M = int(DMM[index-2:index])
    S = round(float(DMM[index:]) * 60, 0)
    print(D, M, S, dir)
    return dms2dd(D, M, S, dir)

def GPS_data_read(lines):
    gprmc = [s for s in lines if "$GPRMC" in s]
    GPS_info = ""
    if gprmc is not None:
        gdata = gprmc[0].split(",")
        status    = gdata[1]
        latitude  = gdata[3]      #latitude
        dir_lat   = gdata[4]      #latitude direction N/S
        longitute = gdata[5]      #longitute
        dir_lon   = gdata[6]      #longitude direction E/W
        speed     = gdata[7]      #Speed in knots
        trCourse  = gdata[8]      #True course
        try:
            receive_t = gdata[1][0:2] + ":" + gdata[1][2:4] + ":" + gdata[1][4:6]
        except ValueError:
            pass
 
        try:
            receive_d = gdata[9][4:] + "/" + gdata[9][2:4] + "/" + gdata[9][0:2] 
        except ValueError:
            pass
        
        print "time : %s, latitude : %s(%s), longitude : %s(%s), speed : %s, True Course : %s, Date : %s" %  (receive_t, latitude , dir_lat, longitute, dir_lon, speed, trCourse, receive_d)
        # GPS_info += '|gps_lat(%s)=%s' % (dir_lat, latitude)
        # GPS_info += '|gps_lon(%s)=%s' % (dir_lon, longitute)
        GPS_info += '|gps_lat=%s' % (dmm2dd(dir_lat, latitude))
        GPS_info += '|gps_lon=%s' % (dmm2dd(dir_lon, longitude))
        return GPS_info
        
def bytes2hex(s):
    return "".join("{:02x}".format(c) for c in s)

def G5T_data_read(dstr):
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
    msg += Conf.others
    
    Restful_URL = Conf.Restful_URL
    print(msg)
    restful_str = "wget -O /tmp/last_upload.log \"" + Restful_URL + "device_id=" + Conf.DEVICE_ID + "&msg=" + msg + "\""
    os.system(restful_str)
 
G5T_RX = 15
GPS_RX = 24
path = "/home/pi/Data/"

########## Start PIGPIO ##########
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
##################################

while True:
    weather_data = ""
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S").split(" ")

    ########## Read GPS ##########
    try:
        pi.bb_serial_read_close(GPS_RX)
    except Exception as e:
        pass
    
    try:
        pi.bb_serial_read_open(GPS_RX, 9600)
        time.sleep(1)
        (GPS_status, GPS_data) = pi.bb_serial_read(GPS_RX)
        if GPS_status:
            print("read GPS")
            lines = ''.join(chr(x) for x in GPS_data).splitlines()
            weather_data += GPS_data_read(lines)
        else:
            print("read nothing")
    except Exception as e:
        print(e)
    
    try:
        pi.bb_serial_read_close(GPS_RX)
        print("GPS close success")
    except Exception as e:
        pass
    ###############################
    print("weather_data: ", weather_data)
    time.sleep(2)

    ########## Reasd G5T ##########
    try:
        pi.bb_serial_read_close(G5T_RX)
    except Exception as e:
        pass

    try:
        pi.bb_serial_read_open(G5T_RX, 9600)
        time.sleep(1)
        (G5T_status, G5T_data) = pi.bb_serial_read(G5T_RX)
        if G5T_status:
            print("read G5T")
            data_hex = bytes2hex(G5T_data)
            weather_data += G5T_data_read(data_hex) 
            if len(weather_data):
                weather_data += '|date=%s' % (str(now_time[0]))
                weather_data += '|time=%s' % (str(now_time[1]))
                upload_data(weather_data)
        else:
            print("read nothing")
 
    except Exception as e:
        print(e)

    try:
        pi.bb_serial_read_close(G5T_RX)
        print("G5T close success")
    except Exception as e: 
        pass
    #############################
    time.sleep(1)
    ########## Store msg ##########
    
    with open(path + str(now_time[0]) + ".txt", "a") as f:
        try:
            if len(weather_data):
                f.write(weather_data + "\n")
        except Exception as e:
            print(e)
            print "Error: writing to SD"    
    ##############################
    time.sleep(5)

pi.stop()
print("End")

