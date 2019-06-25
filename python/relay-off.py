import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

relay = 27

GPIO.setup(relay, GPIO.OUT)
GPIO.output(relay, 0)

GPIO.cleanup()
