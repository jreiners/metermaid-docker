#!/bin/bash

# This generates a weather record every 5 minutes


while :; do python3 /app/bin/weather.py; sleep 300; done

