#!/usr/bin/env bash

# ipmitool -I lanplus -H 192.168.1.189 -U ADMIN -P ADMIN dcmi power reading


SHELL=/bin/sh PATH=/bin:/sbin:/usr/bin:/usr/sbin
MQTT=192.168.1.180
TOPIC1=capteur/electrique/serveur/fan/fan1
TOPIC2=capteur/electrique/serveur/fan/fan2
TOPIC3=capteur/electrique/serveur/fan/fan3
TOPIC4=capteur/electrique/serveur/power
PAYLOAD1=$(ipmitool -I lanplus -H 192.168.1.189 -U ADMIN -P ADMIN sdr entity 29.1 |cut -c 39-42)
PAYLOAD2=$(ipmitool -I lanplus -H 192.168.1.189 -U ADMIN -P ADMIN sdr entity 29.2 |cut -c 39-42)
PAYLOAD3=$(ipmitool -I lanplus -H 192.168.1.189 -U ADMIN -P ADMIN sdr entity 29.3 |cut -c 39-42)
PAYLOAD4=$(ipmitool -I lanplus -H 192.168.1.189 -U ADMIN -P ADMIN dcmi power reading | cut -c 52-54 | head -2 |tail -1)
# echo mosquitto_pub -r -t “$TOPIC1” -m “$PAYLOAD1” -h $MQTT -u "billyboy85" -P "66446644"
mosquitto_pub -r -t $TOPIC1 -m “$PAYLOAD1” -h $MQTT -u "billyboy85" -P "66446644"
mosquitto_pub -r -t $TOPIC2 -m “$PAYLOAD2” -h $MQTT -u "billyboy85" -P "66446644"
mosquitto_pub -r -t $TOPIC3 -m “$PAYLOAD3” -h $MQTT -u "billyboy85" -P "66446644"
mosquitto_pub -r -t $TOPIC4 -m “$PAYLOAD4” -h $MQTT -u "billyboy85" -P "66446644"
