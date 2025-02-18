#!/usr/bin/python

import time
import paho.mqtt.client as mqtt
import re

SERVEUR = '192.168.1.180'
user = 'billyboy85'
pwd = '66446644'

def collectteleinfodata():

    try:
        trame_teleinfo = getteleinfo()  # // recupere une trame teleinfo
        timestamp = time.time()
        base = re.sub('`^[0]*`', '',trame_teleinfo['BaseTarif'])
        va = re.sub('`^[0]*`', '',trame_teleinfo['puissanceApparente'])
        iinst = re.sub('`^[0]*`', '',trame_teleinfo['intensiteInstant'])
        # watt = iinst * 220; // intensite; en; A; X; 220; V // stock; les; donnees
        watt = int(iinst) * 230
        teleinfo_line = '[{"timestamp": "\'%s\'" , "base": "\'%s\'" ,"va": "\'%s\'","iinst": "\'%s\'","watt": "\'%s\'"}]'
        var = (timestamp, base, va, iinst, watt)
        new_line = teleinfo_line % var
        topic = ("capteur/electrique/teleinfo/puissance")
        client.publish(topic, new_line, 1)


    except:
        print("erreur de lecture de trame")


def getteleinfo():

    try:
        handle = open('/dev/ttyAMA0', "r")  # // ouverture du flux
        data = {}
        while True:
            line = handle.readline().strip()
            array = line.split(' ')
            if len(array) > 1:
                header, value = array[0], array[1]
                # Si ADCO 2 fois alors tour complet
                if header == "ADCO":
                    if 'adresseConcentrateur' in data: break
                    data['adresseConcentrateur'] = value
                elif header == "OPTARIF":
                    data['optionTarif'] = value
                elif header == "BASE":
                    data['BaseTarif'] = value
                elif header == "PTEC":
                    data['periodeTarifaire'] = value
                elif header == "IINST":
                    data['intensiteInstant'] = value
                elif header == "ADPS":
                    data['avertissementDepassement'] = value
                elif header == "PAPP":
                    data['puissanceApparente'] = value
                elif header == "IMAX":
                    data['intensiteMaximum'] = value
                elif header == "ISOUSC":
                    data['intensiteSouscrit'] = value
                elif header == "HCHC":
                    data['heuresCreuses'] = value
                elif header == "HCHP":
                    data['heuresPleines'] = value
        return data

    except:
        print("erreur parsing trame")


while True:
    client = mqtt.Client()
    # Set access token
    client.username_pw_set(user, pwd)
    # client.username_pw_set(ACCESS_TOKEN)
    client.connect(SERVEUR, 1883, 60)
    client.loop_start()
    # print("read_temp_raw")
    collectteleinfodata()
    client.loop_stop()
    client.disconnect()
    time.sleep(60)
