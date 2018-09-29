#!/usr/bin/python
####### Developed by Gopal(grajaram@dxc.com)
# This script will analyze the Temperature, Moisture, Photosensitive data which was received from sensors and make a notification to the users if it reaches the defined threshold value
#  Before executing make sure to edit the configure as per your environment like MQTT server user id/password in iot_preempt_settings.py file
#
# Last updated on 22-May-2018

import simplejson as json
import paho.mqtt.client as mqtt
import sys
import WeatherDataFetch
import iot_preempt_settings

##Get the data from config file 
mqtt_server_host=iot_preempt_settings.mqtt_server_host
mqtt_userid=iot_preempt_settings.mqtt_userid
mqtt_password=iot_preempt_settings.mqtt_password
#latlang="12.944342,80.122726"
latlang=iot_preempt_settings.user_latlang


#######Declaraction 
temperature_threshold=30 # increase to match 
humidity_threshold=60    # decrease to match 
photosensitive_threshold=150  

internal_url=0

if(len(sys.argv) > 1):
    mqtt_server_host = sys.argv[1]
    internal_url=1

count=0
email_body="<b><font color=red>Action Required: </font> <font color=blue>Our NextGen-IoT System Predicts Possibility of Fungus Formation in your Home</font></b><br><br>This alert is based on the Temperature, Humidity, Photosensitive sensor data from your home and compared with the weather data based on your GEO location for the next couple of days.<br>Please take appropriate action so that your home is properly ventilated, air circulation is maintained and enough sunlight enters into the rooms.<br><br>Contact:Gopal(grajaram@dxc.com)<br> DXC.Technology"

print "\n\nAnalyzing Home Sensor Data:\n"
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("\tMQTT Server Connected code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("ZF_Sensor_data")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg): 
#    print(msg.topic+" "+str(msg.payload))
    try:
        data = 	json.loads(str(msg.payload))
    except:
	## e.g. Not valid Json={"d":{"name":"Home ID 1", "temp":24.5, "humidity":47.1,"light":}, "timestamp":"2017-03-08 13:56:04.880939","latlang":"12.944342,80.122726"}

        print "Not valid Json="+str(msg.payload)
    triggering_flag=0
    temperature = data["d"]["temp"]
    humidity = data["d"]["humidity"]
    lightingLevel = data["d"]["light"]
    latlang= data["latlang"]
    tcolor="green"
    hcolor="green"
    pcolor="green"
    print 'Cloud: DeviceID: {} Temperature: {} Humidity: {} PhotoSensitive: {}'.format(data["d"]["name"], temperature, humidity, lightingLevel)
    if(temperature <temperature_threshold):
        triggering_flag=1
        tcolor="red"
    if(humidity > humidity_threshold):
        triggering_flag=1
        hcolor="red"        
    if(lightingLevel < photosensitive_threshold):
        triggering_flag=1
        pcolor="red"
 
    collect_json= '{}:{}|{}:{}|{}:{}'.format(tcolor,temperature, hcolor, humidity, pcolor, lightingLevel)
#    print "Before Publishing="+ collect_json
    client.publish("ZF_Monitor_Data_1234", collect_json)
    if(temperature <temperature_threshold) and (humidity > humidity_threshold) and (lightingLevel < photosensitive_threshold):
#        print "triggering_flag=1"
        global count
        count += 1
        if(count >= 5): #defined hour how long it should wait and validate
            print "Looking for Weather API Data ... Location:",latlang,"\n"
            WeatherDataFetch.main(latlang, email_body, internal_url) ## Calling Weather API data for next 3 days 			
            sys.exit()


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(mqtt_userid, mqtt_password)
try:
    client.connect(mqtt_server_host, 1883, 60)
except:
    print "MQTT not connected or No Internet Connection available"
    sys.exit()

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
