from gpiozero import MotionSensor
from picamera import PiCamera
from datetime import datetime
from time import sleep

camera = PiCamera()
pir = MotionSensor(4)
while True:
    pir.wait_for_motion()
    camera.start_preview()
    pir.wait_for_no_motion()
    sleep(6.5)
    camera.stop_preview()
