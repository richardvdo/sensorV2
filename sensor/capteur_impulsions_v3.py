#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import datetime
import paho.mqtt.client as mqtt
import var

compteur_principal = 0.0
compteur = 0
dateJour = 0


def cb_compteur_principal(channel):
    global compteur
    global compteur_principal
    global dateJour
    now = datetime.datetime.now()
    if now.strftime('%d') != dateJour:
        client = mqtt.Client()
        client.username_pw_set(var.user, var.pwd)
        client.connect(var.SERVEUR, 1883, 60)
        client.loop_start()
        dateJour = now.strftime('%d')
        dateveille = now - datetime.timedelta(1)
        dateveille1 = dateveille.strftime('%Y-%m-%d')
        timestampveille = time.mktime(datetime.datetime.strptime(dateveille1, "%Y-%m-%d").timetuple())
        # insertline = "insert into solaire_v1.puissance(timestamp, watt) VALUES('%s', '%s')"
        insertline = '[{"timestamp": "\'%s\'" , "watt": "\'%s\'" }]'
        var = (timestampveille, float(compteur_principal) / 1000.0)
        new_line = insertline % var
        topic = ("capteur/electrique/solaire/puissance")
        client.publish(topic, new_line, 1)
        dateJour = now.strftime('%d')
        compteur_principal = 1
        compteur = 0
        client.loop_stop()
        client.disconnect()
    else:
        compteur_principal = compteur_principal + 1
    compteur = compteur + 1
    if compteur == 100:
        client = mqtt.Client()
        client.username_pw_set(var.user, var.pwd)
        client.connect(var.SERVEUR, 1883, 60)
        client.loop_start()
        timestamp = time.mktime(datetime.datetime.now().timetuple())
        # insertline = "insert into solaire_v1.production(timestamp, watt, watt_totale) VALUES('%s',100,'%s')"
        insertline = '[{"timestamp": "\'%s\'" , "watt": "100" ,"watt_totale": "\'%s\'"}]'
        var = (timestamp, float(compteur_principal) / 1000.0)
        new_line = insertline % var
        topic = ("capteur/electrique/solaire/production")
        client.publish(topic, new_line, 1)
        compteur = 0
        client.loop_stop()
        client.disconnect()


GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(18, GPIO.FALLING, callback=cb_compteur_principal, bouncetime=70)

while True:
    time.sleep(0.1)
