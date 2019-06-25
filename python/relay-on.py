#This script is set up to turn on 1 relay

import RPi.GPIO as GPIO

#sets as gpio number
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

relay = 27

GPIO.setup(relay, GPIO.OUT)

GPIO.output(relay, 1)

