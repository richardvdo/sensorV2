import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BCM)
Relais1 = 12
Relais2 = 16
Relais3 = 20
Relais4 = 21


GPIO.setup(Relais1, GPIO.OUT)
GPIO.setup(Relais2, GPIO.OUT)
GPIO.setup(Relais3, GPIO.OUT)
GPIO.setup(Relais4, GPIO.OUT)

GPIO.output(Relais1, False)
GPIO.output(Relais2, False)
GPIO.output(Relais3, False)
GPIO.output(Relais4, False)


def lumiere_sam():
    GPIO.output(Relais1, True)
    time.sleep(0.1)
    GPIO.output(Relais1, False)


def radiateur_sdb_on():
    GPIO.output(Relais2, True)


def radiateur_sdb_off():
    GPIO.output(Relais2, False)


def na_1():
    GPIO.output(Relais3, False)


def na_2():
    GPIO.output(Relais4, False)


def relais_case(argument):
    switcher = {
        1: lumiere_sam,
        2: radiateur_sdb_on,
        3: radiateur_sdb_off,
        4: na_1,
        5: na_2
    }
    # Get the function from switcher dictionary
    func = switcher.get(argument, lambda: "Invalid month")
    # Execute the function
    func()


if __name__ == '__main__':
    relais_case(sys.argv[1])
    GPIO.cleanup()
