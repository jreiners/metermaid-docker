import requests
import simplejson as json
import mysql.connector


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
                              host='weatherdb',
                              database='metermaid')
print('inserting data')
#print(q)
print('opening cursor.')
cursor = cnx.cursor()
print('executing mysql insert')
cursor.execute(q)
print('committing')
#cursor.commit()
#cursor.close()
cnx.commit()
cnx.close()
print('received json:')
print(weatherjson)
