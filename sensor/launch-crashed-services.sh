#!/bin/bash

service teleinfo status | grep 'active (running)' > /dev/null 2>&1

if [ $? != 0 ]
then
        sudo service teleinfo restart > /dev/null
fi

service solaired status | grep 'active (running)' > /dev/null 2>&1

if [ $? != 0 ]
then
        sudo service solaired restart > /dev/null
fi

service humsensor status | grep 'active (running)' > /dev/null 2>&1

if [ $? != 0 ]
then
        sudo service humsensor restart > /dev/null
fi

service tempsensor status | grep 'active (running)' > /dev/null 2>&1

if [ $? != 0 ]
then
        sudo service tempsensor restart > /dev/null
fi

service ha-bridge status | grep 'active (running)' > /dev/null 2>&1

if [ $? != 0 ]
then
        sudo service ha-bridge restart > /dev/null
fi


# ajout a faire 
# sudo crontab -e
# */1 * * * * /opt/launch-crashed-services.sh > /dev/null 2>
