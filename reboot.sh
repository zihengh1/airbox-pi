#!/bin/bash

value="$(cat ../Local/a.txt)"

sleep 5
[ -f /home/pi/airbox-pi/PiM25.py ] && {
    /usr/bin/git -C /home/pi/airbox-pi fetch origin
    /usr/bin/git -C /home/pi/airbox-pi reset --hard origin/master
    /usr/bin/nohup python -u /home/pi/airbox-pi/PiM25.py &
} || {
    /usr/bin/git clone value /home/pi/airbox-pi
    /usr/bin/nohup python -u /home/pi/airbox-pi/PiM25.py &
}

