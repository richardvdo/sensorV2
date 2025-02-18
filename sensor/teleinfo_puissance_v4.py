#!/usr/bin/python

import time
import paho.mqtt.client as mqtt
import re
import var



def collectteleinfodata():

    global trame_teleinfo
    print(" \n appel de get teleinfo \n")
    trame_teleinfo = getteleinfo()  # // recupere une trame teleinfo
    print(" \n sortie de get teleinfo \n")
    timestamp = time.time()
    base = re.sub('`^[0]*`', '',trame_teleinfo['BASE'])
    va = re.sub('`^[0]*`', '',trame_teleinfo['PAPP'])
    iinst = re.sub('`^[0]*`', '',trame_teleinfo['IINST'])
    # watt = iinst * 220; // intensite; en; A; X; 220; V // stock; les; donnees
    watt = iinst * 230
    print(" \n valeur \n")
    print(timestamp)
    print(base)
    print(va)
    print(iinst)
    print(watt)

    teleinfo_line = '[{"timestamp": "\'%s\'" , "base": "\'%s\'" ,"va": "\'%s\'","iinst": "\'%s\'","watt": "\'%s\'"}]'
    var = (timestamp, base, va, iinst, watt)
    new_line = teleinfo_line % var
    print(new_line)
    topic = ("capteur/electrique/teleinfo/puissance")
    client.publish(topic, new_line, 1)


def getteleinfo():

    global trame
    global char
    global datas
    # char = ''
    lettre_mod = ' '
    lettre = ' '
    log_trame = open('/tmp/trame.log', "a")
    log_trame.write("\n")
    print(" \n ouverture du fichger \n")
    handle = open('/dev/ttyAMA0', "r")  # // ouverture du flux
    print(" \n on attend la fin d'une trame pour commencer a avec la trame suivante \n")
    while lettre_mod != "2":  # // on attend la fin d'une trame pour commencer a avec la trame suivante
        lettre = handle.read(1)
        if len(lettre) > 0:
            lettre_mod = format(ord(lettre))
        char = ''  # essayer de faire le handle read sur une new variable "lettre" et si pas vide faire un format(ord(lettre)) et travailler avec ca pour les tests et avec l'autre pour ecrire
        trame = ''
        datas = ''
        while lettre_mod != "2":  # // on lit tous les caracteres jusqu'a la fin de la trame chr(2)
            lettre = handle.read(1)
            if lettre_mod != "2":
                print("if \n")
                print(lettre != "2")
                print(lettre + "\n")
                print(lettre_mod != "2")
                print(lettre_mod + "\n")
                trame += lettre
                log_trame.write(lettre)
    print(" \n trame : \n")
    print(trame)
    log_trame.write("\n trame : " + trame + "\n")
    log_trame.close()
    handle.close()  # // on ferme le flux
    print(" \n on ferme le fichier \n")
    trame = trame.rstrip()  # on supprime les caracteres de fin de trame
    print(" \n on ferme le fichier \n")
    trame = trame[1:-1]  # // on supprime les caracteres de debut
    messages = trame.split(chr(10))  # // on separe les messages de la trame
    print(" \n messagessss : \n")
    print(messages)
    for message in messages:
        # message = message.split(' ')[-3]  # // on separe l'etiquette, la valeur et la somme de controle de chaque message
        message_cut = message.split(' ')
        print(" \n message_cut \n")
        print(message_cut)
        if message_cut[0] and message_cut[1]:
            etiquette = message_cut[0]
            valeur = message_cut[1]
            print(" \n etiquette \n")
            print(etiquette)
            print(" \n valeur \n")
            print(valeur)
            datas[etiquette] = valeur  # // on stock les etiquettes et les valeurs de l'array datas
    print(" \n datas: \n")
    print(datas)
    return datas


while True:
    print(" \n debut \n")
    client = mqtt.Client()
    # Set access token
    # client.username_pw_set(ACCESS_TOKEN)
    client.username_pw_set(var.user, var.pwd)
    client.connect(var.SERVEUR, 1883, 60)
    client.loop_start()
    # print("read_temp_raw")
    print(" \n connecte et appel de fonction \n")
    collectteleinfodata()
    client.loop_stop()
    client.disconnect()
    print(" \n fin et sleep \n")
    time.sleep(60)
