from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import traceback

from lib.PiM25_config import plot_path
import lib.epaper.epd2in7 as epd2in7

try:
    epd = epd2in7.EPD()

    ## Initialize ##
    epd.init()

    ## Clear screen ##
    epd.Clear(0xFF)

    ## Drawing information ##
    Himage1 = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)
    draw = ImageDraw.Draw(Himage1)

    bmp = Image.open(plot_path + 'Sinica.bmp')
    Himage1.paste(bmp, (55,10))
       
    ## Display ##
    epd.display(epd.getbuffer(Himage1))
        
    ## Sleep ##
    epd.sleep()
        
except Exception as e:
    print(e)

