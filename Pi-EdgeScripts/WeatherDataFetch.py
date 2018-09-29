#!/usr/bin/python

# This script will fetch weather data from a third party vendor based on user GEO location

# Before executing make sure to edit the configure as per your environment like MQTT server user id/password in iot_preempt_settings.py file
#
# Last updated on 22-May-2018

import requests
import datetime
import sys
import PushNotification
import PushWeatherNotify
import send_email
import json
import time

print "Start Time=",str(datetime.datetime.now())

temperature_threshold=38 # increase to match 
humidity_threshold=22  # decrease to match 

def main(latlang, email_body, internal_url):
    host=""
    if latlang is None:
        latlang = "lat=12.944342&lon=80.122726" # MEPZ Location
        print "Defual latlang assigned"
    else:
        #if(len(sys.argv) > 1):
        lat,lon=latlang.split(",")
        latlang="lat="+lat+"&lon="+lon
        print "Location fetching from Arguments\n"
        #else:
        #    latlang = "lat=12.944342&lon=80.122726" # MEPZ Location
        #    print "Defualt Location assigned\n"
    place ="q=Chennai,IN"

    if(internal_url):
        with open('/home/pi/Zurich/ForecastWeatherAPIdata.json') as data_file:
            data=json.load(data_file)
    else:
    
#        url = host + latlang + token + mode
        url = "https://funguslosspredictdev.eu-gb.mybluemix.net/tjson" # Weather simulator data
        print url
    
        response = requests.get(url, verify=True)
        if response.status_code != 200:
            print('Status:', response.status_code, 'Problem with the request. Exiting.')
            exit()
        data = response.json()
    
    forecast = data['list']
    
    Day_Count=0
    Notify_flag=0
    print "\nFetching Weather API data from ", host, "\n"
    for f1 in forecast:
    #   print f1,"\n"
        d1 = datetime.datetime.fromtimestamp(f1["dt"])
        temperature = f1["temp"]["day"]
        humidity = f1["humidity"]
        Day_Count+=1
        print 'Analyzing Weather Day {} Data'.format(Day_Count)
        print "\tDay ", Day_Count,":", d1," Temperature: ", temperature, "\tHumidity: ",humidity 
#        print Notify_flag,"\n"
        if(temperature <temperature_threshold) and (humidity > humidity_threshold):
           Notify_flag=1
#           time.sleep(5)          
        else:
           Notify_flag=0	
           break
    	
        if(Day_Count>=3):
            break
#    Notify_flag=0	
    if(Notify_flag):
        print "Sending Mobile Push Notification ...\n"
        PushNotification.msg()
        PushWeatherNotify.weather_data_msg("weather_not_ok")
        print "Sending Email Notification ...\n"		
#Commented by Gopal 
#        send_email.send_email(email_body)
        #+".<br>Also Weather Forecast Temperature will be less than <b>{}</b> degree Celsius for the next couple of days<br>".format(temperature_threshold)
    else:
        print "\nClimate is goog based on Weather data, so no action required\n"
        PushWeatherNotify.weather_data_msg("weather_is_ok") 
###Needs to comment the below line
#main("12.944342,80.122726", "Test email", True)
 
'''
    {"city":{"id":1253454,"name":"Vandalur","coord":{"lon":80.080833,"lat":12.89278},"country":"IN","population":0},"cod":"200","message":0.0365,"cnt":7,"list":[{"dt":1486965600,"temp":{"day":29,"min":19.43,"max":29,"night":19.43,"eve":27.04,"morn":29},"pressure":1017.48,"humidity":45,"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}],"speed":5.02,"deg":69,"clouds":0},{"dt":1487052000,"temp":{"day":32.21,"min":21.36,"max":31.69,"night":23.02,"eve":28.29,"morn":21.36},"pressure":1021.2,"humidity":49,"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}],"speed":4.61,"deg":36,"clouds":0},{"dt":1487138400,"temp":{"day":31.1,"min":20.53,"max":31.6,"night":20.53,"eve":28.76,"morn":22.63},"pressure":1021.26,"humidity":45,"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}],"speed":5.46,"deg":64,"clouds":0},{"dt":1487224800,"temp":{"day":29.53,"min":20.24,"max":29.53,"night":21.6,"eve":28.18,"morn":20.24},"pressure":1023.03,"humidity":0,"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}],"speed":4.91,"deg":66,"clouds":0},{"dt":1487311200,"temp":{"day":29.35,"min":19.49,"max":29.35,"night":21.4,"eve":28.51,"morn":19.49},"pressure":1021.99,"humidity":0,"weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10d"}],"speed":4.26,"deg":58,"clouds":0},{"dt":1487397600,"temp":{"day":29.43,"min":18.42,"max":29.43,"night":21.11,"eve":29.36,"morn":18.42},"pressure":1021.82,"humidity":0,"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}],"speed":2.63,"deg":88,"clouds":0},{"dt":1487484000,"temp":{"day":29.7,"min":18.07,"max":29.7,"night":21.02,"eve":29.67,"morn":18.07},"pressure":1022.08,"humidity":0,"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}],"speed":1.79,"deg":164,"clouds":0}]}
    
    
'''
    
    

