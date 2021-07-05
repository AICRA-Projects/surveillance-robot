from flask import Flask, render_template, Response
from flask import Flask, render_template, request, redirect, url_for, make_response
import cv2
import cv2 as cv
import smbus
import time
import RPi.GPIO as GPIO
import time
addr = 0x8
channel = 1
bus = smbus.SMBus(channel)
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
maxTime = 0.04
#GPIO.setup(ledpin,GPIO.OUT)

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def writenumber(val):
    bus.write_byte(addr,val)
    return -1
def stringtobyte(val):
    ret =[]
    for i in val:
        ret.append(ord(i))
    return ret


def distance():
    try:
        while(True):
            GPIO.output(GPIO_TRIGGER, False)
            time.sleep(0.01)
    # set Trigger to HIGH
            GPIO.output(GPIO_TRIGGER, True)
    # set Trigger after 0.01ms to LOW
            time.sleep(0.00001)
            GPIO.output(GPIO_TRIGGER, False)
 
            pulse_start = time.time()
            timeout = pulse_start + maxTime

    # save StartTime
            while GPIO.input(GPIO_ECHO) == 0 and pulse_start < timeout:
                pulse_start = time.time()
    
 
            pulse_stop = time.time()
            timeout = pulse_stop + maxTime
    # save time of arrival
            while GPIO.input(GPIO_ECHO) == 1 and pulse_stop < timeout:
                pulse_stop = time.time()
               # time difference between start and arrival
            TimeElapsed = pulse_stop - pulse_start
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
            distance = (TimeElapsed * 34300) / 2
 
            return distance
    except:
        GPIO.cleanup()

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

app = Flask(__name__)

@app.route('/')
def intro():
    in1 = 0
    writenumber(in1)
    return render_template('index.html')

@app.route('/dashboard.html')
def begin():
    in2 = 1
    writenumber(in2)
    return render_template('dashboard.html')

@app.route("/automatic.html")
def auto():
    return render_template("automatic.html")

def face():
    faceCascade = cv2.CascadeClassifier('/home/pi/Downloads/opencv-master/data/haarcascades/haarcascade_frontalface_default.xml')
    vcap = cv2.VideoCapture(0)
    bi_ksize=15
    threshold=25
    sigma=10
    while True:
            ret, img = vcap.read()
            img = cv2.flip(img, -1)
            im_bi = cv2.bilateralFilter(img, bi_ksize, sigma, sigma)
            faces = faceCascade.detectMultiScale(
                im_bi,     
                scaleFactor=1.2,
                minNeighbors=5,     
                minSize=(20, 20)
            )
            in_out = 17
            writenumber(in_out)
            for (x,y,w,h) in faces:
                print(len(faces))
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                crop_img = im_bi[y:y+h, x:x+w]
                gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
                thresholded = cv2.threshold(gray, threshold, 255, 0)[1]
                contours,hierarchy = cv2.findContours(thresholded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                cnt = contours[0]
                area = cv.contourArea(cnt)
                rct = w*h
                abh = area/w*h
                ab = 100-(abh*0.001)
                cv2.putText(img,str(ab),(x, y-50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
                
                if (x > 0 and x < 100) and (y > 0 and y < 160):
                    data = "left upward "
                    cv2.putText(img,str(data),(x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                    if ab > -25 and ab < 60:
                        rob = "near"
                        in_out=6
                        writenumber(in_out)
                        cv2.putText(img,str(rob),(x, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                    elif ab > 60 and ab < 100:
                        rob = "accept"
                        in_out=8
                        writenumber(in_out)
                        cv2.putText(img,str(rob),(x, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                    else:
                        rob = "reject"
                        in_out=7
                        writenumber(in_out)
                        cv2.putText(img,str(rob),(x, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                elif x > 300 and (y > 0 and y < 160):
                    data = "right Upward"
                    cv2.putText(img,str(data),(x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                    if ab > -25 and ab < 60:
                        rob = "near"
                        in_out=6
                        writenumber(in_out)
                        cv2.putText(img,str(rob),(x, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                    elif ab > 60 and ab < 100:
                        rob = "accept"
                        in_out=9
                        writenumber(in_out)
                        cv2.putText(img,str(rob),(x, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                    else:
                        rob = "reject"
                        in_out=7
                        writenumber(in_out)
                        cv2.putText(img,str(rob),(x, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
 
                elif (x > 100 and x < 300 ) and (y > 0 and y < 160):
                        data = "upward"
                        cv2.putText(img,str(data),(x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                        if ab > -25 and ab < 60:
                            rob = "near"
                            in_out=6
                            writenumber(in_out)
                            cv2.putText(img,str(rob),(x, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                        elif ab > 60 and ab < 100:
                            rob = "accept"
                            in_out=5
                            writenumber(in_out)
                            cv2.putText(img,str(rob),(x, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                        else:
                            rob = "reject"
                            in_out=7
                            writenumber(in_out)
                            cv2.putText(img,str(rob),(x, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                elif (x > 0 and x < 100 ) and (y > 160 and y <320):
                    data = "left"
                    cv2.putText(img,str(data),(x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                    if ab > -25 and ab < 60:
                        rob = "near"
                        in_out=6
                        writenumber(in_out)
                        cv2.putText(img,str(rob),(x, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                    elif ab > 60 and ab < 100:
                        rob = "accept"
                        in_out=3
                        writenumber(in_out)
                        cv2.putText(img,str(rob),(x, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                    else:
                        rob = "reject"
                        in_out=7
                        writenumber(in_out)
                        cv2.putText(img,str(rob),(x, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                elif (x > 100 and x < 300) and (y > 160 and y < 320):
                    data="Front"
                    cv2.putText(img, str(data),(x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                    if ab > -25 and ab < 60:
                        rob = "near"
                        in_out=6
                        writenumber(in_out)
                        cv2.putText(img,str(rob),(x, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                    elif ab > 60 and ab < 100:
                        rob = "accept"
                        in_out=5
                        writenumber(in_out)
                        cv2.putText(img,str(rob),(x, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                    else:
                        rob = "reject"
                        in_out=7
                        writenumber(in_out)
                        cv2.putText(img,str(rob),(x, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                elif x > 300 and (y > 160 and y < 320):
                    data="right"
                    cv2.putText(img, str(data),(x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                    if ab > -25 and ab < 60:
                        rob = "near"
                        in_out=6
                        writenumber(in_out)
                        cv2.putText(img,str(rob),(x, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                    elif ab > 60 and ab < 100:
                        rob = "accept"
                        in_out=4
                        writenumber(in_out)
                        cv2.putText(img,str(rob),(x, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                    else:
                        rob = "reject"
                        in_out=7
                        writenumber(in_out)
                        cv2.putText(img,str(rob),(x, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                elif (x > 0 and x < 100) and (y > 320 and y < 480):
                    data = "left downward"
                    cv2.putText(img,str(data),(x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                    if ab > -25 and ab < 60:
                        rob = "near"
                        in_out=6
                        writenumber(in_out)
                        cv2.putText(img,str(rob),(x, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                    elif ab > 60 and ab < 100:
                        rob = "accept"
                        in_out=3
                        writenumber(in_out)
                        cv2.putText(img,str(rob),(x, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                    else:
                        rob = "reject"
                        in_out=7
                        writenumber(in_out)
                        cv2.putText(img,str(rob),(x, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                elif (x > 100 and x < 300) and (y > 320 and y < 480):
                    data = "downward"
                    cv2.putText(img,str(data),(x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                    if ab > -25 and ab < 60:
                        rob = "near"
                        in_out=6
                        writenumber(in_out)
                        cv2.putText(img,str(rob),(x, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                    elif ab > 60 and ab < 100:
                        rob = "accept"
                        in_out=6
                        writenumber(in_out)
                        cv2.putText(img,str(rob),(x, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                    else:
                        rob = "reject"
                        in_out=7
                        writenumber(in_out)
                        cv2.putText(img,str(rob),(x, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                elif (x > 300) and (y > 320 and y < 480):
                        data = "right downward"
                        cv2.putText(img,str(data),(x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                        if ab > -25 and ab < 60:
                            rob = "near"
                            in_out=6
                            writenumber(in_out)
                            cv2.putText(img,str(rob),(x, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                        elif ab > 60 and ab < 100:
                            rob = "accept"
                            in_out=4
                            writenumber(in_out)
                            cv2.putText(img,str(rob),(x, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                        else:
                            rob = "reject"
                            in_out=7
                            writenumber(in_out)
                            cv2.putText(img,str(rob),(x, y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                else:
                    in_out=7
                    writenumber(in_out) 
            ret, jpeg = cv2.imencode('.jpg', img)
        #get camera frame
            fram = jpeg.tobytes()
 
            yield (b'--fram\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + fram + b'\r\n\r\n')
        





    
@app.route("/face_feed")                                         
def face_feed():
        return Response(face(),
                mimetype='multipart/x-mixed-replace; boundary=fram')




@app.route('/manual.html')
def manual_mode():
    in3 = 2
    writenumber(in3)
    return render_template('man.html')
                
@app.route("/video_feed")
def video_feed():
    print('video')
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=fram')

@app.route('/Left',methods=['GET','POST'])
def left():
    in_out=3
    writenumber(in_out)
    res = make_response(redirect(url_for('manual_mode')))
    return (res)

@app.route("/Right",methods=['GET','POST'])
def right():
    in_out=4
    writenumber(in_out)
    res = make_response(redirect(url_for('manual_mode')))
    return res

@app.route("/UpperSide",methods=['GET','POST'])
def forward():
    in_out=5
    writenumber(in_out)
    res = make_response(redirect(url_for('manual_mode')))
    return res
    
@app.route("/Down_Side", methods=['GET','POST'])
def backward():
    in_out=6
    writenumber(in_out)
    res = make_response(redirect(url_for('manual_mode')))
    return res

@app.route("/stop",methods=['GET','POST'])
def stop():
    in_out=7
    writenumber(in_out)
    res = make_response(redirect(url_for('manual_mode')))
    return res

@app.route("/Side_Left", methods=['GET','POST'])
def side_left():
    in_out=8
    writenumber(in_out)
    res = make_response(redirect(url_for('manual_mode')))
    return res


@app.route("/Side_Right", methods=['GET','POST'])
def side_right():
    in_out=9
    writenumber(in_out)
    res = make_response(redirect(url_for('manual_mode')))
    return res


@app.route("/Down_Left", methods=['GET','POST'])
def down_left():
    in_out=10
    writenumber(in_out)
    res = make_response(redirect(url_for('manual_mode')))
    return res


@app.route("/Down_Right", methods=['GET','POST'])
def down_right():
    in_out=11
    writenumber(in_out)
    res = make_response(redirect(url_for('manual_mode')))
    return res

@app.route("/cameraup", methods=['GET','POST'])
def camera_up():
    in_out=12
    writenumber(in_out)
    res = make_response(redirect(url_for('manual_mode')))
    return res

@app.route("/cameradown", methods=['GET','POST'])
def camera_down():
    in_out=13
    writenumber(in_out)
    res = make_response(redirect(url_for('manual_mode')))
    return res




if __name__== '__main__':
    app.run(host='0.0.0.0',threaded=True)
