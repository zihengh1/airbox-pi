import re
import os

GPS_LAT = 25.1933
GPS_LON = 121.7870

# Device information
APP_ID = "PiM25"
DEVICE = "Raspberry Pi 3B+"
DEVICE_ID = "DEVICE_ID1234"
DEVICE_IP = ''

# Restful_API
Restful_URL = "https://data.lass-net.org/Upload/PiM25.php?"
Restful_interval = 60           # 60 seconds
float_re_pattern = re.compile("^-?\d+\.\d+$")
num_re_pattern = re.compile("^-?\d+\.\d+$|^-?\d+$")

# MAC address
mac = open('/sys/class/net/eth0/address').readline().upper().strip()
DEVICE_ID = mac.replace(':','') 
print(DEVICE_ID)

others = '|gps_num=100|s_lr=-1|s_l0=-1|fmt_opt=0|s_lg=-1|tick=0.0|s_lb=-1|s_lc=-1|s_g8=0|ver_format=3|gps_fix=1|ver_app=0.0.1|FAKE_GPS=1'

fields ={       
    "Tmp"   :       "s_t0",           
    "RH"    :       "s_h0",           
    "PM1.0" :       "s_d2",           
    "PM2.5" :       "s_d0",           
    "PM10"  :       "s_d1",              
    "Lux"   :       "s_l0",
    "RGB_R" :       "s_lr",
    "RGB_G" :       "s_lg",
    "RGB_B" :       "s_lb",
    "RGB_C" :       "s_lc",
    "CO2"   :       "s_g8",              
    "TVOC"  :       "s_gg",
}
                                            
values = {      
    "app"           :       APP_ID,      
    "device_id"     :       DEVICE_ID,                  
    "device"        :       DEVICE,                     
    "ver_format"    :       3,                        
    "fmt_opt"       :       0,                        
    "gps_lat"       :       GPS_LAT,                    
    "gps_lon"       :       GPS_LON,                    
    "FAKE_GPS"      :       1,                        
    "gps_fix"       :       1,                        
    "gps_num"       :       100,                      
    "date"          :       "1900-01-01",                        
    "time"          :       "00:00:00",                          
}                       


