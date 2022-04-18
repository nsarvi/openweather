import requests
import datetime
import mysql.connector
from mysql.connector import Error
import GPSLocation
from datetime import timedelta
import time
import os

import json
api_key = os.environ['APIKEY']

# 10 locations
dfw = GPSLocation.GPS("DFW", "37.757815", "-96.9080557")
sfo = GPSLocation.GPS("SFO", "37.6246766", "-122.4071407")
nyc = GPSLocation.GPS("NYC", "40.6976701", "-74.2598705")
ord = GPSLocation.GPS("ORD", "41.8339042", "-88.0121528")
blr = GPSLocation.GPS("BLR", "12.9542946", "77.4908519")
london = GPSLocation.GPS("London", "51.5287352", "-0.3817815")
seatle = GPSLocation.GPS("Seatle", "47.6131746", "-122.4821488")
miami = GPSLocation.GPS("Miami", "25.7825453", "-80.2994991")
austin = GPSLocation.GPS("Austin", "30.3080553", "-98.033596")
vegas = GPSLocation.GPS("Austin", "36.1251958", "-115.3150858")

locationList = []
locationList.append(dfw)
locationList.append(sfo)
locationList.append(nyc)
locationList.append(ord)
locationList.append(blr)
locationList.append(london)
locationList.append(seatle)
locationList.append(miami)
locationList.append(austin)
locationList.append(vegas)

date = datetime.datetime.utcnow()
yesterday = date.today() - timedelta(days=1)
dt = int(time.mktime(yesterday.timetuple()))
date_time = datetime.datetime.fromtimestamp(dt)
print("Getting historical weather data for the Date & Time =>", date_time.strftime('%Y-%m-%d %H:%M:%S'))

try:
    connection = mysql.connector.connect(host='mysql',
                                         database='openweather',
                                         user='test',
                                         password='test')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

        sql = "INSERT INTO weatherhistory (hourlydt, lat, lng , temp , feels_like , pressure , humidity , wind_speed) " \
              "VALUES (%s, %s, %s,%s, %s, %s,%s, %s) "

        for loc in locationList:
            url = "https://api.openweathermap.org/data/2.5/onecall/timemachine?lat=%s&lon=%s&dt=%s&appid=%s&units=imperial" % (
                loc.lat, loc.lon, dt, api_key)
            print("Getting weather data for ", loc.name)
            response = requests.get(url)
            data = json.loads(response.text)
            print(data)
            # insert in batches
            cursor = connection.cursor()
            dailyData = []
            for row in range(len(data['hourly'])):
                tempdt = data['hourly'][row]['dt']
                tstamp = datetime.datetime.fromtimestamp(tempdt)
                print(datetime.datetime.fromtimestamp(tempdt), data['lat'], data['lon'],
                      round(data['hourly'][row]['temp']), data['hourly'][row]['feels_like'],
                      data['hourly'][row]['pressure'], data['hourly'][row]['humidity'],
                      data['hourly'][row]['wind_speed'])
                dailyData.append((tstamp, data['lat'], data['lon'], round(data['hourly'][row]['temp']),
                                  round(data['hourly'][row]['feels_like']), data['hourly'][row]['pressure'],
                                  data['hourly'][row]['humidity'], round(data['hourly'][row]['wind_speed'])))
            cursor.executemany(sql, dailyData)
            cursor.close()

        print("Max temperature by location and month")
        maxTemperatureByMonthCursor = connection.cursor()
        # select lat, lng, extract(year_month from hourlydt) as yearmonth , max(temp) from weatherhistory  group by lat, lng, yearmonth
        maxTemperatureByMonthSQL = "INSERT INTO temperaturebymonth (lat, lng , yearmonth , max_temp) " \
              "select lat, lng, extract(year_month from hourlydt) as yearmonth , max(temp) from weatherhistory  group by lat, lng, yearmonth"
        maxTemperatureByMonthCursor.execute(maxTemperatureByMonthSQL)
        maxTemperaturesByDayCursor = connection.cursor()
        print("Avg,Min, max temperature by location and Day")
        temperaturesByMonthSQL= "INSERT INTO temperaturesbyday (lat, lng , date , avg_temp, min_temp, max_temp) " \
              "select lat, lng, date(hourlydt) as day ,avg(temp), min(temp),  max(temp) from weatherhistory  group by lat, lng, day"
        maxTemperaturesByDayCursor.execute(temperaturesByMonthSQL)
        connection.commit()

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")