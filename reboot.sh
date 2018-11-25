#!/bin/bash

sleep 5
[-f /home/pi/Rescue_CA/test.py ] && {
    # /usr/bin/git -C /home/pi/SensorArray fetch origin
    # /usr/bin/git -C /home/pi/SensorArray reset --hard origin/master
    sudo pigpiod
    nohup python -u /home/pi/Rescue_CA/test.py &
} 

    # || {
    # /usr/bin/git clone https://github.com/zihengh1/SensorArray/ /home/pi/SensorArray
    # nohup python -u /home/pi/SensorArray/sensor.py &
    # }
