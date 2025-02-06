from flask import Flask, render_template, request, abort
from gpiozero import MotionSensor
from picamera import PiCamera
import datetime
from time import sleep
from subprocess import call
import threading

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

homeDir = '/home/pi/webapp/'
imgDir = 'static/img/'
pir = MotionSensor(4)

# Global counter with thread-safe access using a lock
count = 0
count_lock = threading.Lock()

def capture_image(file_path):
    """Encapsulate camera image capture with error handling."""
    try:
        with PiCamera() as camera:
            camera.hflip = True
            camera.capture(file_path)
    except Exception as e:
        app.logger.error(f"Error capturing image: {e}")
        raise

@app.route('/', methods=['GET'])
def index():
    """Home page: Capture and display image with timestamp."""
    file = '10.jpg'
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    image_path = f"{homeDir}{imgDir}{file}"

    try:
        capture_image(image_path)
    except Exception:
        abort(500, description="Camera capture failed")

    templateData = {'title': 'HOME - Bird House', 'time': timeString, 'pic': image_path}
    return render_template('index.html', **templateData)

@app.route('/hello/<name>', methods=['GET'])
def hello(name):
    """Personalized page that captures a new image and greets the user."""
    file = '10.jpg'
    image_path = f"{homeDir}{imgDir}{file}"
    try:
        capture_image(image_path)
    except Exception:
        abort(500, description="Camera capture failed")
    return render_template('page.html', name=name, pic=image_path)

@app.route('/camera', methods=['GET'])
def camera_route():
    """Capture an image after waiting for motion and display it."""
    global count
    # Use a thread-safe counter to generate filenames
    with count_lock:
        count = (count % 10) + 1  # Resets count to 1 after 10
        file = f"{count}.jpg"
    image_path = f"{homeDir}{imgDir}{file}"
    templateData = {'pic': f"{imgDir}{file}"}

    # Wait for motion detection with a timeout; log if no motion is detected
    try:
        motion_detected = pir.wait_for_motion(timeout=5)
        if not motion_detected:
            app.logger.warning("Motion sensor timeout: No motion detected within 5 seconds.")
    except Exception as e:
        app.logger.error(f"Motion sensor error: {e}")

    try:
        capture_image(image_path)
    except Exception:
        abort(500, description="Camera capture failed")

    return render_template('cam.html', **templateData)

@app.route('/live', methods=['GET'])
def live():
    return render_template('live.html')

@app.route('/shutdown', methods=['GET'])
def shutdown():
    call(["sudo shutdown", "-h now"], shell=True)
    return "Shutting Down"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
