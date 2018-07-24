#!/bin/bash

cd ~/twircbot

if [ -f ~/twircbot/twircbot.pid ]; then
	ps up `cat ~/twircbot/twircbot.pid ` >/dev/null || /usr/bin/python3.5 ~/twircbot/twircbot.py >/dev/null
else
	/usr/bin/python3.5 ~/twircbot/twircbot.py >/dev/null
fi
