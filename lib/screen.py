from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time
import traceback
import commands
import re
import json
from urllib2 import urlopen

from PiM25_config import plot_path
import epaper.epd2in7 as epd2in7

def transform_to_bmp():
    file_in = plot_path + "line.png"
    file_out = plot_path + "line.bmp"

    img = Image.open(file_in)
    img = img.convert("L")
    img = img.resize((264, 130), Image.ANTIALIAS)
    img.save(file_out)

def get_city():
    url = "http://ipinfo.io/json"
    response = urlopen(url)
    info = json.load(response)

    city = info['city']
    return city
    
def display(data):
    
    try:
        epd = epd2in7.EPD()

        ## Initialize ##
        epd.init()

        ## Clear screen ##
        epd.Clear(0xFF)

        ## Drawing information ##
        Himage1 = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)
        draw = ImageDraw.Draw(Himage1)
        font_size = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',14)

        ## String format ##        
        app = data["app"]
        city = get_city()
        pm25 = "PM2.5: " + str(data["s_d0"])
        hum = "Hum: " + str(data["s_h0"])
        temp = "Temp: " + str(data["s_t0"])
        ip = commands.getoutput('hostname -I')
        device_id = data["device_id"]
        time_str = data["date"] + " " + data["time"]
        
        ## Draw text ##
        draw.text((3, 0), app, font = font_size, fill = 0)
        draw.text((80, 0), city, font = font_size, fill = 0)
        draw.text((164, 0), device_id, font = font_size, fill = 0)
        draw.text((3, 15), pm25, font = font_size, fill = 0)
        draw.text((107, 15), hum, font = font_size, fill = 0)
        draw.text((200, 15), temp, font = font_size, fill = 0)
        draw.text((3, 30), time_str, font = font_size, fill = 0)
        draw.text((160, 30), ip, font = font_size, fill = 0)
        draw.line((3, 45, 260, 45), fill = 0)
      
        bmp = Image.open(plot_path + 'line.bmp')
        Himage1.paste(bmp, (0,48))
       
        ## Display ##
        epd.display(epd.getbuffer(Himage1))
        
        ## Sleep ##
        epd.sleep()
        
    except Exception as e:
        print(e)

