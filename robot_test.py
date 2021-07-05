from flask import Flask, render_template, Response
import cv2
from flask import Flask, render_template, request, redirect, url_for, make_response
import time
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM) 

ds_factor=0.6

GPIO_TRIGGER = 18
GPIO_ECHO = 24

GPIO_PWM_1 = 12
GPIO_PWM_2 = 13
GPIO_IN1 = 23
GPIO_IN2 = 16
GPIO_IN3 = 20
GPIO_IN4 = 21

GPIO.setup(GPIO_IN1, GPIO.OUT)
GPIO.setup(GPIO_IN2, GPIO.OUT)
GPIO.setup(GPIO_IN3, GPIO.OUT)
GPIO.setup(GPIO_IN4, GPIO.OUT)
GPIO.setup(GPIO_PWM_1, GPIO.OUT)
GPIO.setup(GPIO_PWM_2, GPIO.OUT)

pi_pwm_1 = GPIO.PWM(GPIO_PWM_1,1000)
pi_pwm_1.start(0)
pi_pwm_2 = GPIO.PWM(GPIO_PWM_2,1000)
pi_pwm_2.start(0)
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

app = Flask(__name__)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

def left():
    pi_pwm_1.ChangeDutyCycle(100)
    pi_pwm_2.ChangeDutyCycle(100)
    GPIO.output(GPIO_IN1, True)
    GPIO.output(GPIO_IN2, False)
    GPIO.output(GPIO_IN3, False)
    GPIO.output(GPIO_IN4, False)
    
def right():
    pi_pwm_1.ChangeDutyCycle(100)
    pi_pwm_2.ChangeDutyCycle(100)
    GPIO.output(GPIO_IN1, False)
    GPIO.output(GPIO_IN2, False)
    GPIO.output(GPIO_IN3, True)
    GPIO.output(GPIO_IN4, False)
    
def front():
    pi_pwm_1.ChangeDutyCycle(40)
    pi_pwm_2.ChangeDutyCycle(40)
    GPIO.output(GPIO_IN1, True)
    GPIO.output(GPIO_IN2, False)
    GPIO.output(GPIO_IN3, True)
    GPIO.output(GPIO_IN4, False)

def stop():
    pi_pwm_1.ChangeDutyCycle(0)
    pi_pwm_2.ChangeDutyCycle(0)
    GPIO.output(GPIO_IN1, True)
    GPIO.output(GPIO_IN2, False)
    GPIO.output(GPIO_IN3, True)
    GPIO.output(GPIO_IN4, False)


@app.route("/")
def home():
    stop()
    return render_template("dashboard.html")


@app.route("/automatic.html")
def auto():
    return render_template("automatic.html")

def face():
        video = cv2.VideoCapture(0)
        faceCascade = cv2.CascadeClassifier('/home/pi/Downloads/opencv-master/data/haarcascades/haarcascade_frontalface_default.xml')
        while True:
                ret, frame = video.read()
                img = cv2.flip(frame, -1)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = faceCascade.detectMultiScale(
                    gray,     
                    scaleFactor=1.2,
                    minNeighbors=5,     
                    minSize=(20, 20)
                )
                for (x,y,w,h) in faces:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                #frame=cv2.resize(frame,None,fx=ds_factor,fy=ds_factor, interpo$
                ret, jpeg = cv2.imencode('.jpg', img)
        #get camera frame
                fram = jpeg.tobytes()
 
                yield (b'--fram\r\n'
	         b'Content-Type: image/jpeg\r\n\r\n' + fram + b'\r\n\r\n')



    
@app.route("/face_feed")                                         
def face_feed():
    return Response(face(),
                mimetype='multipart/x-mixed-replace; boundary=fram')

    
        
    


@app.route("/manual.html")
def about():
	 # rendering webpage
    return render_template('manual.html')
def gen():
        video = cv2.VideoCapture(0)
        while True:
                ret, frame = video.read()
                #frame=cv2.resize(frame,None,fx=ds_factor,fy=ds_factor, interpo$
                frame = cv2.flip(frame, -1)
                ret, jpeg = cv2.imencode('.jpg', frame)
        #get camera frame
                fram = jpeg.tobytes()
 
                yield (b'--fram\r\n'
	         b'Content-Type: image/jpeg\r\n\r\n' + fram + b'\r\n\r\n')
                
@app.route("/video_feed")
def video_feed():
    print('video')
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=fram')

@app.route('/left_side', methods=['GET','POST'])
def left_side():
    print('left')
    pi_pwm_1.ChangeDutyCycle(100)
    pi_pwm_2.ChangeDutyCycle(100)
    GPIO.output(GPIO_IN1, True)
    GPIO.output(GPIO_IN2, False)
    GPIO.output(GPIO_IN3, False)
    GPIO.output(GPIO_IN4, False)

    response = make_response(redirect(url_for('about')))
    return (response)

@app.route('/right_side', methods=['GET','POST'])
def right_side():
    print('right')
    pi_pwm_1.ChangeDutyCycle(100)
    pi_pwm_2.ChangeDutyCycle(100)
    GPIO.output(GPIO_IN1, False)
    GPIO.output(GPIO_IN2, False)
    GPIO.output(GPIO_IN3, True)
    GPIO.output(GPIO_IN4, False)
    response = make_response(redirect(url_for('about')))
    return (response)

@app.route('/down_side', methods=['GET','POST'])
def back_side():
    print('back')
    pi_pwm_1.ChangeDutyCycle(80)
    pi_pwm_2.ChangeDutyCycle(80)
    GPIO.output(GPIO_IN1, False)
    GPIO.output(GPIO_IN2, True)
    GPIO.output(GPIO_IN3, False)
    GPIO.output(GPIO_IN4, True)
    response = make_response(redirect(url_for('about')))
    return (response)

@app.route('/up_side', methods=['GET','POST'])
def for_side():
    print('up')
    pi_pwm_1.ChangeDutyCycle(50)
    pi_pwm_2.ChangeDutyCycle(50)
    GPIO.output(GPIO_IN1, True)
    GPIO.output(GPIO_IN2, False)
    GPIO.output(GPIO_IN3, True)
    GPIO.output(GPIO_IN4, False)
    response = make_response(redirect(url_for('about')))
    return (response)
@app.route('/stop', methods=['GET','POST'])
def for_stop():
    print('Stop')
    pi_pwm_1.ChangeDutyCycle(50)
    pi_pwm_2.ChangeDutyCycle(50)
    GPIO.output(GPIO_IN1, False)
    GPIO.output(GPIO_IN2, False)
    GPIO.output(GPIO_IN3, False)
    GPIO.output(GPIO_IN4, False)
    response = make_response(redirect(url_for('about')))
    return (response)

if __name__=="__main__":
	app.run(host='0.0.0.0')
	GPIO.cleanup()