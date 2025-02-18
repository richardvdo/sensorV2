#!/usr/bin/python

from datetime import datetime
from sqlite3 import Timestamp
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import var as mqttvar


compteur = 0.0



def cb_compteur_principal(channel):
    global compteur
    client = mqtt.Client()
    client.username_pw_set(mqttvar.user, mqttvar.pwd)
    client.connect(mqttvar.SERVEUR, 1883, 60)
    client.loop_start()
    dt = datetime.now()
    # getting the timestamp
    # ts = datetime.timestamp(dt)
    insertline = '{"solaire": {"timestamp": "\'%s\'" , "watt": 1, "total": %s }}'
    var = (dt, compteur)
    new_line = insertline % var
    topic = ("capteur/electrique/solaire/puissance")
    client.publish(topic, new_line, 1)
    client.loop_stop()
    client.disconnect()
    compteur = compteur + 0.001


GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(18, GPIO.FALLING, callback=cb_compteur_principal, bouncetime=70)

while True:
    time.sleep(0.1)
