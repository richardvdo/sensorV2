import os
import time
import Adafruit_DHT
import paho.mqtt.client as mqtt

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

SERVEUR = '192.168.1.192'
device_folder = []
device_file = []
temp_c = []
sonde = [['27', 'humidite', 'exterieur']]


def read_hum_raw(pin):

    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pin)

    if humidity is not None:
        # print("hum\\n")
        # print(humidity)
        # print("temp\\n")
        # print(temperature)
        return humidity
    else:
        return "error"


def read_hum():
    try:
        i = 0
        for sensor in sonde:
            lines = read_hum_raw(sonde[i][0])
            # print(lines)
            # print(sonde[i][0])
            # print(sonde[i][1])
            # print(sonde[i][2])

            if lines != 'error':
                # sensor_line = ("insert into sensor_v1.record(timestamp, sensor_name, sensor_type, sensor_place, value) VALUES(NOW(), 'DHT11' , '%s', '%s', '%s')")
                # sensor_line = ("insert into sensor_v1.record(timestamp, sensor_name, sensor_type, sensor_place, value) VALUES(NOW(), 'DHT11' , '%s', '%s', '%s')")
                sensor_line = '[{"nom": "DHT11" , "type_capteur": "\'%s\'" ,"emplacement": "\'%s\'","valeur": "\'%s\'"}]'
                # print(sensor_line)
                var = (sonde[i][1], sonde[i][2], lines)
                # var = ("humi", "gara", lines)
                # print var
                new_line = sensor_line % var
                # print (new_line)
                topic = ("capteur/" + sonde[i][1] + "/" + sonde[i][2])
                # print(new_line)
                # print(topic)
                client.publish(topic, new_line, 1)

    except KeyboardInterrupt:
        pass


while True:
    # print(" \\n boucle \n")
    client = mqtt.Client()
    # Set access token
    # client.username_pw_set(ACCESS_TOKEN)
    client.connect(SERVEUR, 1883, 60)
    client.loop_start()
    # print("read_temp_raw")
    read_hum()
    client.loop_stop()
    client.disconnect()
    time.sleep(60)

