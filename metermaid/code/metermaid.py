#!/usr/bin/env python3
# Depends:
# netcat, rtlamr, rtl_tcp

import subprocess
import socket
import re
import time
import sqlite3
import utility_meters

# Adjustable path variables.

meters = {}
electricMeterTypes = [4, 5, 7, 8]
gasMeterTypes = [2, 9, 12]
waterMeterTypes = [11, 13]

# Executing utility_meters.py to get the modified classes
exec(open("utility_meters.py").read())

# SQLite connection and cursor creation
dbConn = sqlite3.connect("/data/metermaid.db")
dbCur = dbConn.cursor()

# Start the rtl device and server
print("Starting RTL_TCP Out Port 5566")
rtl_tcp = subprocess.Popen("rtl_tcp -p 5566", stdout=subprocess.PIPE, shell=True)
print("Sleeping 15 seconds")
time.sleep(15)

print("Starting RTLAMR In Port 5566; Out on 5577")
print("Starting rtlamr")
rtlamr = subprocess.Popen(
    "rtlamr -server 127.0.0.1:5566 | nc -l -p 5577", stdout=subprocess.PIPE, shell=True
)
print("Sleeping 5 seconds")
time.sleep(5)

rtlSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
rtlSocket.connect(("127.0.0.1", 5577))

rtlSocket.recv(498)  # Skip the initial lines
while True:
    # Receive line, always the same length when using plaintext format
    pkt = rtlSocket.recv(111).decode("ascii")
    rtlSocket.recv(1)  # Receive '\n'
    # print(pkt)
    # Regex split the line; figure out why it sometimes doesn't work
    # {Time:2015-10-10T12:48:47.704 SCM:{ID:42354463 Type: 5 Tamper:{Phy:01 Enc:03} Consumption: 5559353 CRC:0xBB11}}
    try:
        pktRegex = re.search("Time\:(\S+) .+ID\:(\d+) +Type\: *(\d{1,2}) .+Consumption: *(\d+)", pkt)
        pDate = pktRegex.group(1)
        pEpoch = time.mktime(time.strptime(pDate, "%Y-%m-%dT%H:%M:%S.%f"))
        pId = str(pktRegex.group(2))
        pType = str(pktRegex.group(3))
        # Consumption (xxxyy) kWh * 10 = Wh
        pConsumption = int(pktRegex.group(4))
        pWh = pConsumption * 10
    except AttributeError:
        print("Error: Received a corrupted packet from stream")
        continue

    # Electric; type 4, 5, 7, 8
    if int(pType) in electricMeterTypes:
        if pId not in meters:
            meters[pId] = ElectricMeter(pId, pType, pEpoch, pWh, dbCur)
        watts = meters[pId].getCurrentWatts(pEpoch, pWh)

    # Gas; type 2, 9, 12
    elif int(pType) in gasMeterTypes:
        if pId not in meters:
            meters[pId] = GasMeter(pId, pType, pEpoch, pConsumption, dbCur)
        gasPerSec = meters[pId].getGasPerSec(pEpoch, pConsumption)

    # Water; type 11, 13
    elif int(pType) in waterMeterTypes:
        if pId not in meters:
            meters[pId] = WaterMeter(pId, pType, pEpoch, pConsumption, dbCur)
        waterPerSec = meters[pId].getWaterPerSec(pEpoch, pConsumption)
    else:
        print("Meter type not recognized")
