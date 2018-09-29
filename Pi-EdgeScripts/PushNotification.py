#!/usr/bin/python
# This script will notifiy the enduser about the chances of Mold/Fungus growth in their homes/buildings
# Before executing make sure to edit the configure as per your environment like MQTT server user id/password in iot_preempt_settings.py file
#
# Last updated on 22-May-2018

import paho.mqtt.client as mqtt
import iot_preempt_settings

mqtt_server_host=iot_preempt_settings.mqtt_server_host
mqtt_userid=iot_preempt_settings.mqtt_userid
mqtt_password=iot_preempt_settings.mqtt_password

#mqtt_server_host="192.168.0.101"

def on_connect(client, userdata, flags, rc):
    print("\tMQTT Server Connected code "+str(rc))

#    client.subscribe("Pi_ZF_Sensor_data")

#def on_message(client, userdata, msg):
#    print(msg.topic+" "+str(msg.payload))



#client.loop_forever()
def msg():
    client = mqtt.Client()
    client.on_connect = on_connect
    #client.on_message = on_message
    client.username_pw_set(mqtt_userid, mqtt_password) 
    client.connect(mqtt_server_host, 1883, 60)
    print "Pushing messgae to "+ mqtt_server_host + "\n"
    client.publish("ZF_Mobile_Notify_1234", "Action Required: Our NextGen-IoT System Predicts Possibility of Fungus Formation in your Home")
    client.disconnect()
#msg() 
