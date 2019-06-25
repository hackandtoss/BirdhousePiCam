from gpiozero import MotionSensor
from picamera import PiCamera
from datetime import datetime

camera = PiCamera()
pir = MotionSensor(4)
while True:
    pir.wait_for_motion()
    start = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
    print(start)
    pir.wait_for_no_motion()
    stop = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
    print(stop)
