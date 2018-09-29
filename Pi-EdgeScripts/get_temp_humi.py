#!/usr/bin/python
####### Developed by Gopal(grajaram@dxc.com)
# This script will fetch Temperature, Moisture, Photosensitive data values from various sensors and published in a MQTT Server
# Before executing make sure to edit the configure as per your environment like MQTT server user id/password in iot_preempt_settings.py file
#
# Last updated on 22-May-2018

import sys
sys.path.append("/home/pi/Adafruit_Python_DHT")
import Adafruit_DHT
import paho.mqtt.client as mqtt
import datetime
import serial
import iot_preempt_settings

mqtt_server_host=iot_preempt_settings.mqtt_server_host
mqtt_userid=iot_preempt_settings.mqtt_userid
mqtt_password=iot_preempt_settings.mqtt_password
#latlang="12.944342,80.122726"
latlang=iot_preempt_settings.user_latlang

if(len(sys.argv) > 1):
    mqtt_server_host=sys.argv[1]

port = serial.Serial("/dev/ttyACM0", baudrate = 9600, timeout=None)

def on_connect(client, userdata, flags, rc):
    print("\tMQTT Server Connected code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
#    client.subscribe("Pi_ZF_Sensor_data")

# The callback for when a PUBLISH message is received from the server.
#def on_message(client, userdata, msg):
#    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
#client.on_message = on_message
client.username_pw_set(mqtt_userid, mqtt_password)
client.connect(mqtt_server_host, 1883, 60)

#client.loop_forever()

#humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 4)
#var_temp = '"temp": {0:0.1f}'.format(temperature) 
#var_temp2 = ', "humidity": {0:0.1f}'.format(humidity) 



while True:
#    humidity, temperature =0,0
    lighting_level=port.readline()[0:-2]
#    lighting_level.rstrip('\r\n')
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 4)
 #   print 'Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity)
    var_temp = '{0:0.1f}'.format(temperature) 
    var_temp2 = '{0:0.1f}'.format(humidity)  
    timestamp = str(datetime.datetime.now())
    if lighting_level == "":
        lighting_level="0"	
    collect_json = '{"d":{"name":"Home ID 1", "temp":' + var_temp + ', "humidity":'+ var_temp2 + ',"light":'+ lighting_level +'}, "timestamp":"'+ timestamp + '","latlang":"' + latlang  +'"}'
    print " Client: Temperature: "+ var_temp +", Humidity:" + var_temp2 + ", Light: " + lighting_level +" " + timestamp[0:-7]
    #print collect_json
    client.publish("ZF_Sensor_data", collect_json)
 

