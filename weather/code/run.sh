#!/bin/bash

# This generates a weather record every 5 minutes


echo "weather script is waiting 30 seconds for sql to start"
sleep 30
echo "starting weather recorder"
while :; do python3 /app/bin/weather.py; sleep 300; done

