#!/usr/bin/env bash

# ipmitool -I lanplus -H 192.168.1.189 -U ADMIN -P ADMIN dcmi power reading


SHELL=/bin/sh PATH=/bin:/sbin:/usr/bin:/usr/sbin
MQTT=192.168.1.61
TOPIC1=capteur/electrique/serveur/info
#TOPIC4=capteur/electrique/serveur/power
PAYLOAD1=$(ipmitool -I lanplus -H 192.168.1.189 -U ADMIN -P ADMIN sdr entity 29.1 |cut -c 39-42)
PAYLOAD2=$(ipmitool -I lanplus -H 192.168.1.189 -U ADMIN -P ADMIN sdr entity 29.2 |cut -c 39-42)
PAYLOAD3=$(ipmitool -I lanplus -H 192.168.1.189 -U ADMIN -P ADMIN sdr entity 29.3 |cut -c 39-42)
PAYLOAD4=$(ipmitool -I lanplus -H 192.168.1.189 -U ADMIN -P ADMIN dcmi power reading | cut -c 52-54 | head -2 |tail -1)


PAYLOAD="{\"fan1\":$PAYLOAD1, \"fan2\":$PAYLOAD2, \"fan3\":$PAYLOAD3, \"power\":$PAYLOAD4 }"

echo mosquitto_pub -r -t “$TOPIC1” -m "$PAYLOAD" -h $MQTT -u "billyboy85" -P "66446644"

mosquitto_pub -r -t $TOPIC1 -m "$PAYLOAD" -h $MQTT -u "billyboy85" -P "66446644"

# mosquitto_pub -r -t $TOPIC4 -m “$PAYLOAD4” -h $MQTT -u "billyboy85" -P "66446644"
