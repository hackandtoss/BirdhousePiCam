from flask import Flask, render_template, request
from gpiozero import MotionSensor
from picamera import PiCamera
import datetime
from time import sleep
from subprocess import call

count = 0
homeDir = '/home/pi/webapp/'
imgDir = 'static/img/'
pir = MotionSensor(4)
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def index():
    global homeDir
    global imgDir
    file = '10.jpg'
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    image = homeDir + imgDir + file
    templateData = {'title': 'HOME - Bird House', 'time': timeString, 'pic': image}
    with PiCamera() as camera:
        camera.hflip = True
        camera.capture(templateData['pic'])
    return render_template('index.html', **templateData, methods=['GET', 'POST'])

@app.route('/hello/<name>')
def hello(name):
    global homeDir
    global imgDir
    file = '10.jpg'
    image = homeDir + imgDir + file
    with PiCamera() as camera:
        camera.hflip = True
        camera.capture(image)
    return render_template('page.html', name=name, methods=['GET', 'POST'])

@app.route('/camera')
def image():
    global count
    global homeDir
    global imgDir
    count += 1
    if (count > 10):
        count = 1
    file = str(count) + ".jpg"
    image = homeDir + imgDir + file
    templateData = {'pic': imgDir + file}
    pir.wait_for_motion(timeout=5)
    with PiCamera() as camera:
        camera.hflip = True
        camera.capture(image)
    return render_template('cam.html',**templateData, methods=['GET', 'POST'])

@app.route('/live')
def live():
    return render_template('live.html', methods=['GET', 'POST'])

@app.route('/shutdown')
def shutdown():
    call(["sudo shutdown", "-h now"], shell=True)
    return "Shutting Down"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')