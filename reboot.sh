#!/bin/bash

sleep 5
[ -f /home/pi/airbox-pi/PiM25.py ] && {
    /usr/bin/git -C /home/pi/airbox-pi fetch origin
    /usr/bin/git -C /home/pi/airbox-pi reset --hard origin/master
    echo "Program start"
    /usr/bin/python -u /home/pi/airbox-pi/PiM25.py &> /dev/null
} || {
    /usr/bin/git clone https://github.com/zihengh1/airbox-pi/ /home/pi/airbox-pi
    echo "Program start"
    /usr/bin/python -u /home/pi/airbox-pi/PiM25.py &> /dev/null
}
