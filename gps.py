import time
import pigpio
import commands

RX = 24
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
    try:
        pi.bb_serial_read_open(RX, 9600)
        time.sleep(0.9)
        (status, data) = pi.bb_serial_read(RX)
        if status:
            print("read_something")
            lines = ''.join(chr(x) for x in data)
            print(lines)
        else:
            print("read nothing")
 
    except Exception as e:
        print(e)
        pi.bb_serial_read_close(RX)
        print("close success")

    pi.bb_serial_read_close(RX)
    time.sleep(5)

pi.stop()
print("End")

