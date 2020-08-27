import os
import glob
import time
import paho.mqtt.client as mqtt
import json
import sys

SERVEUR = '192.168.1.192'

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

device_folder = []
device_file = []
temp_c = []
# sonde = [['28-0517c1764bff', 'temperature', 'garage']]
sonde = [['28-0517c1764bff', 'temperature', 'garage'], ['28-0417c13d9dff', 'temperature', 'exterieur']]
base_dir = '/sys/bus/w1/devices/'
end_dir = '/w1_slave'


for device in sonde:
    if os.path.exists(str(base_dir) + device[0]):
        device_folder.append(str(base_dir) + device[0])

for folder in device_folder:
    device_file.append(str(folder) + end_dir)


def read_temp_raw(file):
    f = open(file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    try:
        i = 0
        for sensor in device_file:
            if os.path.exists(sensor):
                lines = read_temp_raw(sensor)
                while lines[0].strip()[-3:] != 'YES':
                    time.sleep(0.2)
                    lines = read_temp_raw()
                    equals_pos = lines[1].find('t=')
                    if equals_pos != -1:
                        temp_string = lines[1][equals_pos+2:]
                        temp_c.append(float(temp_string) / 1000.0)

                        sensor_line = "{\"capteur\": [{\"nom\": \"'%s'\" \"capteur\": \"'%s'\",\"emplacement\": \"'%s'\",\"valeur\": \"'%s'\"}]}"
                        var = (sensor, sonde[i][1], sonde[i][2], (float(temp_string) / 1000.0))
                        new_line = sensor_line % var
                        topic=("capteur\\" + sonde[i][1] + "\\" + sonde[i][2])
                        client.publish(topic, json.dumps(new_line), 1)
                        i = i + 1
    except KeyboardInterrupt:
        pass


while True:
    client = mqtt.Client()
    # Set access token
    # client.username_pw_set(ACCESS_TOKEN)
    client.connect(SERVEUR, 1883, 60)
    client.loop_start()
    read_temp()
    client.loop_stop()
    client.disconnect()
    time.sleep(60)
