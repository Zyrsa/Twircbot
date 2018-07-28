#!/bin/bash

cd ~/twircbot

if [ -f ~/twircbot/run.pid ]; then
	ps up `cat ~/twircbot/run.pid ` >/dev/null || /usr/bin/python3.5 ~/twircbot/twircbot.py >/dev/null
else
	/usr/bin/python3.5 ~/twircbot/twircbot.py >/dev/null
fi
