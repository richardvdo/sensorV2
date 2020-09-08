#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import datetime
import paho.mqtt.client as mqtt
import re


def collectteleinfodata():

    # $link = mysqli_connect('192.168.1.56', 'pi', '66446644', 'teleinfo_v2') \
    #        or die('Impossible de se connecter : '.mysqli_error());

    # $query = 'CREATE TABLE IF NOT EXISTS puissance (timestamp INTEGER, base INTEGER, va REAL, iinst REAL, watt REAL);';
    # $result = mysqli_query($link,$query) or die('Échec de la requête : '.mysqli_error($link));

    trame = getteleinfo() # // recupere une trame teleinfo

    timestamp = time()
    # base = preg_replace('`^[0]*`', '',$trame['BASE']); // conso total en Wh, on supprime les 0 en debut de chaine
    base = re.sub('`^[0]*`', '',trame['BASE']) # // conso total en Wh, on supprime les 0 en debut de chaine
    # va = preg_replace('`^[0]*`', '',$trame['PAPP']); // puissance; en; V.A, on; supprime; les; 0; en; debut; de; chaine
    va = re.sub('`^[0]*`', '',trame['PAPP']) # // puissance; en; V.A, on; supprime; les; 0; en; debut; de; chaine
    # iinst = preg_replace('`^[0]*`', '',$trame['IINST']); // intensité; instantanée; en; A, on; supprime; les; 0; en; debut; de; chaine
    iinst = re.sub('`^[0]*`', '',trame['IINST'])  # // intensité; instantanée; en; A, on; supprime; les; 0; en; debut; de; chaine
    # watt = iinst * 220; // intensite; en; A; X; 220; V // stock; les; donnees
    watt = iinst * 220 #// intensite; en; A; X; 220; V // stock; les; donnees


    # $query = "INSERT INTO puissance (timestamp, base, va, iinst, watt) VALUES (" + timestamp + ", '" + base + "', " + va + ", " + iinst + ", " + watt + ")"
    # $result = mysqli_query($link,$query) or die('Échec de la requête : '.mysqli_error($link));

    teleinfo_line = '[{"timestamp": "\'%s\'" , "base": "\'%s\'" ,"va": "\'%s\'","iinst": "\'%s\'","watt": "\'%s\'"}]'
    var = (timestamp, base, va, iinst, watt)
    new_line = teleinfo_line % var
    topic = ("capteur/electrique/teleinfo/puissance")
    client.publish(topic, new_line, 1)


def getteleinfo() :

    $handle = fopen ('/dev/ttyAMA0', "r"); // ouverture du flux

    if (!$handle) die ("'/dev/ttyAMA0' not found");

    while (fread($handle, 1) != chr(2)); // on attend la fin d'une trame pour commencer a avec la trame suivante

    $char  = '';
    $trame = '';
    $datas = '';

    while ($char != chr(2)) { // on lit tous les caracteres jusqu'a la fin de la trame
      $char = fread($handle, 1);
      if ($char != chr(2)){
        $trame .= $char;
      }
    }

    fclose ($handle); // on ferme le flux

    $trame = chop(substr($trame,1,-1)); // on supprime les caracteres de debut et fin de trame

    $messages = explode(chr(10), $trame); // on separe les messages de la trame

    foreach ($messages as $key => $message) {
      $message = explode (' ', $message, 3); // on separe l'etiquette, la valeur et la somme de controle de chaque message
      if(!empty($message[0]) && !empty($message[1])) {
        $etiquette = $message[0];
        $valeur    = $message[1];
        $datas[$etiquette] = $valeur; // on stock les etiquettes et les valeurs de l'array datas
      }
    }
    return datas


while True:
    # print(" \\n boucle \n")
    client = mqtt.Client()
    # Set access token
    # client.username_pw_set(ACCESS_TOKEN)
    client.connect(SERVEUR, 1883, 60)
    client.loop_start()
    # print("read_temp_raw")
    read_temp()
    client.loop_stop()
    client.disconnect()
    time.sleep(60)