import os
import glob
import time
import mysql.connector
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
# sonde[0] = '28-0517c1764bff'
# sonde[1] = '28-0417c13d9dff'
# sonde2 = ''
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


client = mqtt.Client()
# Set access token
# client.username_pw_set(ACCESS_TOKEN)

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(SERVEUR, 1883, 60)
client.loop_start()

try:
    while True:
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
                        # conn = mysql.connector.connect(host="maison.lithium", user="pi", password="66446644", database="sensor_v1")
                        # cursor = conn.cursor()
                        sensor_line = ("insert into sensor_v1.record(timestamp, sensor_name, sensor_type, sensor_place, value) VALUES(NOW(), '%s' , '%s', '%s', '%s')")
                        var = (sensor, sonde[i][1], sonde[i][2], (float(temp_string) / 1000.0))
                        new_line = sensor_line % var
                        client.publish('test_channel', json.dumps(new_line), 1)
                        i = i + 1
                        # conn.close()
                        new_line = []
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
time.sleep(600)