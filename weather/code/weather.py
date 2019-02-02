import requests
import simplejson as json
import mysql.connector

createdb="CREATE DATABASE IF NOT EXISTS metermaid;"
createtbl1="CREATE TABLE IF NOT EXISTS `utilities` (`mPrimaryKey` int(6) unsigned NOT NULL AUTO_INCREMENT,`mId` varchar(50) DEFAULT NULL,`mType` int(2) DEFAULT NULL,`mTime` int(11) DEFAULT NULL, `mTotalConsumption` int(11) DEFAULT NULL,`mConsumed` float DEFAULT NULL,PRIMARY KEY (`mPrimaryKey`)) ENGINE=InnoDB AUTO_INCREMENT=1408484 DEFAULT CHARSET=latin1 ROW_FORMAT=COMPRESSED;"
createtbl2="CREATE TABLE IF NOT EXISTS `weatherdb` (`id` int(11) NOT NULL AUTO_INCREMENT,`epoch` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(), `mintemp` float DEFAULT NULL, `maxtemp` float DEFAULT NULL, `currenttemp` float DEFAULT NULL, `windspeed` float DEFAULT NULL, `winddir` varchar(3) DEFAULT NULL, `text1` varchar(30) DEFAULT NULL, `text2` varchar(30) DEFAULT NULL, PRIMARY KEY (`id`)) ENGINE=InnoDB AUTO_INCREMENT=57915 DEFAULT CHARSET=latin1 ROW_FORMAT=COMPRESSED;"


url='http://api.openweathermap.org/data/2.5/weather?q=Omaha&appid=fd3a41ccb4f3d1242381c0d007883e4d&units=imperial'

response = requests.get(url, verify=True) #Verify is check SSL certificate

weatherjson = response.content

j = json.loads(response.content)

min=j['main']['temp_min']
max=j['main']['temp_max']
currenttemp=j['main']['temp']
windspeed=j['wind']['speed']
winddir=j['wind']['deg']
describe=j['weather'][0]['description']
main=j['weather'][0]['main']


q = "INSERT INTO metermaid.weatherdb (epoch, mintemp, maxtemp,currenttemp,windspeed,winddir,text1,text2) VALUES(NOW(),'{}','{}','{}','{}','{}','{}','{}');".format(min,max,currenttemp,windspeed,winddir,describe,main)

cnx = mysql.connector.connect(user='root', password='weatherdb',
                              host='127.0.0.1',
                              database='metermaid')
print('inserting data')
#print(q)
print('opening cursor.')
cursor = cnx.cursor()
cursor.execute(createdb)
cursor.execute(createtbl1)
cursor.execute(createtbl2)

print('executing mysql insert')
cursor.execute(q)
print('committing')
#cursor.commit()
#cursor.close()
cnx.commit()
cnx.close()
print('received json:')
print(weatherjson)
