from flask import Flask, render_template, Response
import cv2
from flask import Flask, render_template, request, redirect, url_for, make_response
import time
import RPi.GPIO as GPIO

ds_factor=0.6
mA1=18
mA2=23
mB1=24
mB2=25
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(mA1, GPIO.OUT)
GPIO.setup(mA2, GPIO.OUT)
GPIO.setup(mB1, GPIO.OUT)
GPIO.setup(mB2, GPIO.OUT)
GPIO.output(mA1 , 0)
GPIO.output(mA2 , 0)
GPIO.output(mB1, 0)
GPIO.output(mB2, 0)


app = Flask(__name__)

def face():
    faceCascade = cv2.CascadeClassifier('/home/pi/Downloads/opencv-master/data/haarcascades/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    while True:
        succ, img = cap.read()
        img = cv2.flip(img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,     
            scaleFactor=1.2,
            minNeighbors=5,     
            minSize=(20, 20)
        )
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
        succ, jpg = cv2.imencode('.jpg', img)
        ram = jpg.tobytes()
        yield (b'--fram\r\n'
	 b'Content-Type: image/jpeg\r\n\r\n' + ram + b'\r\n\r\n')

@app.route("/")
def home():
	return render_template("aicra.html")


@app.route("/automatic")
def auto():
	return render_template("video.html")

@app.route("/face_feed")
def face_feed():
    print('facevideo')
    return Response(face(),
                    mimetype='multipart/x-mixed-replace; boundary=ram')


@app.route("/manual")
def about():
	 # rendering webpage
    return render_template('robot.html')
def gen():
        video = cv2.VideoCapture(0)
        while True:
                ret, frame = video.read()
                #frame=cv2.resize(frame,None,fx=ds_factor,fy=ds_factor, interpo$
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
    response = make_response(redirect(url_for('about')))
    return (response)

@app.route('/right_side', methods=['GET','POST'])
def right_side():
    print('right')
    response = make_response(redirect(url_for('about')))
    return (response)

@app.route('/down_side', methods=['GET','POST'])
def back_side():
    print('back')
    response = make_response(redirect(url_for('about')))
    return (response)

@app.route('/up_side', methods=['GET','POST'])
def for_side():
    print('up')
    response = make_response(redirect(url_for('about')))
    return (response)



if __name__=="__main__":
	app.run(host='0.0.0.0')