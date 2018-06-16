# MeterMaid

This is a fork of utility-mon from https://github.com/benvandoren. I modified this code release because I use grafana to graph my power and gas use, so I didnt need the web pieces. I have made some modifications of the original, as the mType was being appended to the end of the mId.


Most of the hard work goes to benvandoren. Thank you.

# Installation:
installation requires Python3, requests, simplejson,mysql.connector, subprocess, socket, re, time, pymysql.


# WeatherDB create table

```
   CREATE DATABASE weather;

   CREATE TABLE `weatherdb` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `epoch` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `mintemp` float DEFAULT NULL,
  `maxtemp` float DEFAULT NULL,
  `currenttemp` float DEFAULT NULL,
  `windspeed` float DEFAULT NULL,
  `winddir` varchar(3) DEFAULT NULL,
  `text1` varchar(30) DEFAULT NULL,
  `text2` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=78 DEFAULT CHARSET=latin1 ROW_FORMAT=COMPRESSED
```

# UtilityMeter create table

```
   CREATE DATABASE UtilityMon;
   
   CREATE TABLE `UtilityMeter` (
  `mPrimaryKey` int(6) unsigned NOT NULL AUTO_INCREMENT,
  `mId` varchar(50) DEFAULT NULL,
  `mType` int(2) DEFAULT NULL,
  `mTime` int(11) DEFAULT NULL,
  `mTotalConsumption` int(11) DEFAULT NULL,
  `mConsumed` float DEFAULT NULL,
  PRIMARY KEY (`mPrimaryKey`)
) ENGINE=InnoDB AUTO_INCREMENT=135144 DEFAULT CHARSET=latin1 ROW_FORMAT=COMPRESSED
```

# MySQL grants

`grant all privileges on weather.Weatherdb identified by 'password';`

`grant all privileges on UtilityMon.UtilityMeter identified by 'password';`

Make sure you edit database.py with your current mysql credentials you just set up.




# Grafana statements!

Electric Meter:

```
SELECT
  mId as metric,
  mTime as time_sec,
  mConsumed as value
FROM UtilityMon.UtilityMeter
WHERE
  mId=5744xxxx
and
  $__unixEpochFilter(mTime)
;
```

Gas Meter:

```
SELECT
  mId as metric,
  mTime as time_sec,
  mConsumed as value
FROM UtilityMon.UtilityMeter
WHERE
  mId=6592xxxx
and
  $__unixEpochFilter(mTime)
;
```

Neighborhood Electric Meters:

```
SELECT
  mType,
  mId as metric,
  mTime as time_sec,
  mConsumed as value
FROM UtilityMon.UtilityMeter
WHERE
  mType=7
and
  $__unixEpochFilter(mTime)
;
```

Neighborhood Gas Meters:

```
SELECT
  mType,
  mId as metric,
  mTime as time_sec,
  mConsumed as value
FROM UtilityMon.UtilityMeter
WHERE
  mType=12
and
  $__unixEpochFilter(mTime)
;
```

Weather:
I'll update this when I get it implemented.

Use:
clone somewhere

`vim /etc/systemd/system/UtilityMon.service`

```
[Unit]
Description=MeterMaid
After=network.target

[Service]
Type=simple
User=reiners.io
WorkingDirectory=/home/reiners.io
ExecStart=/home/reiners.io/bin/utilitymon.py
Restart=on-abort

[Install]
WantedBy=multi-user.target
```

`vim /etc/systemd/system/weather.service`


```
[Unit]
Description=weather
After=network.target

[Service]
Type=simple
User=reiners.io
WorkingDirectory=/home/reiners.io
ExecStart= 'while true do; python3 /home/reiners.io/bin/weather.py; sleep 900; done'
Restart=on-abort

[Install]
WantedBy=multi-user.target
```

`systemctl enable weather.service`

`systemctl enable UtilityMon.service`

`systemctl start weather`

`systemctl start UtilityMon`

Sample data:

weather table:

```
mysql> select * from weatherdb limit 5;
+----+---------------------+---------+---------+-------------+-----------+---------+-----------+-------+
| id | epoch               | mintemp | maxtemp | currenttemp | windspeed | winddir | text1     | text2 |
+----+---------------------+---------+---------+-------------+-----------+---------+-----------+-------+
| 10 | 0000-00-00 00:00:00 |     1.4 |    10.4 |        6.24 |     11.41 | 340     | clear sky | Clear |
| 11 | 2018-02-06 00:58:59 |     1.4 |    10.4 |        6.42 |     11.41 | 340     | clear sky | Clear |
| 12 | 2018-02-06 00:59:13 |     1.4 |    10.4 |        6.24 |     11.41 | 340     | clear sky | Clear |
| 13 | 2018-02-06 00:59:16 |     1.4 |    10.4 |        6.42 |     11.41 | 340     | clear sky | Clear |
| 14 | 2018-02-06 00:59:18 |     1.4 |    10.4 |        6.24 |     11.41 | 340     | clear sky | Clear |
+----+---------------------+---------+---------+-------------+-----------+---------+-----------+-------+
```

Meter table:

```
mysql> select * from UtilityMeter limit 5;
+-------------+-----------+-------+------------+-------------------+-----------+
| mPrimaryKey | mId       | mType | mTime      | mTotalConsumption | mConsumed |
+-------------+-----------+-------+------------+-------------------+-----------+
|           1 | 574481377 |     7 | 1517464663 |          44661240 |   1069.31 |
|           2 | 574378957 |     7 | 1517464665 |          39391750 |       840 |
|           3 | 319978947 |     7 | 1517464670 |          22393060 |   596.026 |
|           4 | 319978767 |     7 | 1517464675 |          60909230 |       360 |
|           5 | 574383587 |     7 | 1517464675 |          99609330 |   1184.21 |
+-------------+-----------+-------+------------+-------------------+-----------+
5 rows in set (0.00 sec)
```

