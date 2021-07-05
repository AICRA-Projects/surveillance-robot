from flask import Flask, render_template, Response
from flask import Flask, render_template, request, redirect, url_for, make_response
import cv2
import cv2 as cv
import smbus
import numpy as np
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
    in2 = 14
    writenumber(in2)
    return render_template('dashboard.html')

@app.route("/automatic.html")
def auto():
    return render_template("automatic.html")

@app.route("/color-detection.html")
def colo():
    return render_template("color-detection.html")

@app.route("/auto-pilot.html")
def autopi():
    return render_template("auto-pilot.html")


def face():
    faceCascade = cv2.CascadeClassifier('/home/pi/Downloads/opencv-master/data/haarcascades/haarcascade_frontalface_default.xml')
    tap = cv2.VideoCapture(0)
    bi_ksize=15
    threshold=25
    sigma=10
    while True:
            et, imgfr = tap.read()
            imgfr = cv2.flip(imgfr, -1)
            im_bi = cv2.bilateralFilter(imgfr, bi_ksize, sigma, sigma)
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
                cv2.rectangle(imgfr,(x,y),(x+w,y+h),(255,0,0),2)
       
                if (x > 0 and x < 100) and (y > 0 and y < 160):
                    data = "left upward "
                    in_out=3
                    writenumber(in_out)
                    cv2.putText(imgfr,str(data),(x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                    
                elif x > 300 and (y > 0 and y < 160):
                    data = "right Upward"
                    in_out=4
                    writenumber(in_out)
                    cv2.putText(imgfr,str(data),(x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                    
 
                elif (x > 100 and x < 300 ) and (y > 0 and y < 160):
                    data = "upward"
                    in_out=5
                    writenumber(in_out)
                    cv2.putText(imgfr,str(data),(x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                       
                elif (x > 0 and x < 100 ) and (y > 160 and y <320):
                    data = "left"
                    in_out=3
                    writenumber(in_out)
                    cv2.putText(imgfr,str(data),(x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
               
                elif (x > 100 and x < 300) and (y > 160 and y < 320):
                    data="Front"
                    in_out=5
                    writenumber(in_out)
                    cv2.putText(imgfr, str(data),(x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                    
                elif x > 300 and (y > 160 and y < 320):
                    data="right"
                    in_out=4
                    writenumber(in_out)
                    cv2.putText(imgfr, str(data),(x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                   
                elif (x > 0 and x < 100) and (y > 320 and y < 480):
                    data = "left downward"
                    in_out=3
                    writenumber(in_out)
                    cv2.putText(imgfr,str(data),(x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                  
                elif (x > 100 and x < 300) and (y > 320 and y < 480):
                    data = "downward"
                    in_out=5
                    writenumber(in_out)
                    cv2.putText(imgfr,str(data),(x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
           
                elif (x > 300) and (y > 320 and y < 480):
                    data = "right downward"
                    in_out=4
                    writenumber(in_out)
                    cv2.putText(imgfr,str(data),(x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
                else:
                    in_out=7
                    writenumber(in_out) 
            et, jpe = cv2.imencode('.jpg', imgfr)
        #get camera frame
            frm = jpe.tobytes()
 
            yield (b'--frm\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frm + b'\r\n\r\n')


def auto():
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
            dist = distance()
            if dist < 50:
                in_out = 17
                writenumber(in_out)
                if len(faces) > 0:
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
                                
                elif dist < 50 and len(faces) == 0:
                    print("no faces")
                    in_out = 18
                    writenumber(in_out)
            elif dist > 50:
                print("no obstacle")
                in_out = 15
                writenumber(in_out)
            ret, jpeg = cv2.imencode('.jpg', img)
        #get camera frame
            fram = jpeg.tobytes()
 
            yield (b'--fram\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + fram + b'\r\n\r\n')
        

def color():
        # Capturing video through webcam 
    webcam = cv2.VideoCapture(0) 

    # Start a while loop 
    while(1): 
        
        # Reading the video from the 
        # webcam in image frames 
        re, imageFrame = webcam.read() 

        # Convert the imageFrame in 
        # BGR(RGB color space) to 
        # HSV(hue-saturation-value) 
        # color space 
        hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV) 

        # Set range for red color and 
        # define mask 
        red_lower = np.array([136, 87, 111], np.uint8) 
        red_upper = np.array([180, 255, 255], np.uint8) 
        red_mask = cv2.inRange(hsvFrame, red_lower, red_upper) 

        # Set range for green color and 
        # define mask 
        green_lower = np.array([25, 52, 72], np.uint8) 
        green_upper = np.array([102, 255, 255], np.uint8) 
        green_mask = cv2.inRange(hsvFrame, green_lower, green_upper) 

        # Set range for blue color and 
        # define mask 
        blue_lower = np.array([94, 80, 2], np.uint8) 
        blue_upper = np.array([120, 255, 255], np.uint8) 
        blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper) 
        
        # Morphological Transform, Dilation 
        # for each color and bitwise_and operator 
        # between imageFrame and mask determines 
        # to detect only that particular color 
        kernal = np.ones((5, 5), "uint8") 
        
        # For red color 
        red_mask = cv2.dilate(red_mask, kernal) 
        res_red = cv2.bitwise_and(imageFrame, imageFrame, 
                                mask = red_mask) 
        
        # For green color 
        green_mask = cv2.dilate(green_mask, kernal) 
        res_green = cv2.bitwise_and(imageFrame, imageFrame, 
                                    mask = green_mask) 
        
        # For blue color 
        blue_mask = cv2.dilate(blue_mask, kernal) 
        res_blue = cv2.bitwise_and(imageFrame, imageFrame, 
                                mask = blue_mask) 

        # Creating contour to track red color 
        contours, hierarchy = cv2.findContours(red_mask, 
                                            cv2.RETR_TREE, 
                                            cv2.CHAIN_APPROX_SIMPLE) 
        
        for pic, contour in enumerate(contours): 
            area = cv2.contourArea(contour) 
            if(area > 300): 
                x, y, w, h = cv2.boundingRect(contour) 
                imageFrame = cv2.rectangle(imageFrame, (x, y), 
                                        (x + w, y + h), 
                                        (0, 0, 255), 2) 
                
                cv2.putText(imageFrame, "Red Colour", (x, y), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, 
                            (0, 0, 255))	 

        # Creating contour to track green color 
        contours, hierarchy = cv2.findContours(green_mask, 
                                            cv2.RETR_TREE, 
                                            cv2.CHAIN_APPROX_SIMPLE) 
        
        for pic, contour in enumerate(contours): 
            area = cv2.contourArea(contour) 
            if(area > 300): 
                x, y, w, h = cv2.boundingRect(contour) 
                imageFrame = cv2.rectangle(imageFrame, (x, y), 
                                        (x + w, y + h), 
                                        (0, 255, 0), 2) 
                
                cv2.putText(imageFrame, "Green Colour", (x, y), 
                            cv2.FONT_HERSHEY_SIMPLEX, 
                            1.0, (0, 255, 0)) 

        # Creating contour to track blue color 
        contours, hierarchy = cv2.findContours(blue_mask, 
                                            cv2.RETR_TREE, 
                                            cv2.CHAIN_APPROX_SIMPLE) 
        for pic, contour in enumerate(contours): 
            area = cv2.contourArea(contour) 
            if(area > 300): 
                x, y, w, h = cv2.boundingRect(contour) 
                imageFrame = cv2.rectangle(imageFrame, (x, y), 
                                        (x + w, y + h), 
                                        (255, 0, 0), 2) 
                
                cv2.putText(imageFrame, "Blue Colour", (x, y), 
                            cv2.FONT_HERSHEY_SIMPLEX, 
                            1.0, (255, 0, 0))
        
        re, peg = cv2.imencode('.jpg',imageFrame)
        #get camera frame
        ram = peg.tobytes()
 
        yield (b'--ram\r\n'
    b'Content-Type: image/peg\r\n\r\n' + ram + b'\r\n\r\n')


@app.route("/color_feed")
def color_feed():
        return Response(color(),
                mimetype='multipart/x-mixed-replace; boundary=ram')
    
@app.route("/auto_feed")
def auto_feed():
    return Response(auto(),
            mimetype='multipart/x-mixed-replace; boundary=fram')
    
@app.route("/face_feed")                                         
def face_feed():
        return Response(face(),
                mimetype='multipart/x-mixed-replace; boundary=frm')




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
    in_out=22
    writenumber(in_out)
    res = make_response(redirect(url_for('manual_mode')))
    return (res)

@app.route("/Right",methods=['GET','POST'])
def right():
    in_out=23
    writenumber(in_out)
    res = make_response(redirect(url_for('manual_mode')))
    return res

@app.route("/UpperSide",methods=['GET','POST'])
def forward():
    in_out=20
    writenumber(in_out)
    res = make_response(redirect(url_for('manual_mode')))
    return res
    
@app.route("/Down_Side", methods=['GET','POST'])
def backward():
    in_out=21
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
    in_out=25
    writenumber(in_out)
    res = make_response(redirect(url_for('manual_mode')))
    return res


@app.route("/Side_Right", methods=['GET','POST'])
def side_right():
    in_out=24
    writenumber(in_out)
    res = make_response(redirect(url_for('manual_mode')))
    return res


@app.route("/Down_Left", methods=['GET','POST'])
def down_left():
    in_out=26
    writenumber(in_out)
    res = make_response(redirect(url_for('manual_mode')))
    return res


@app.route("/Down_Right", methods=['GET','POST'])
def down_right():
    in_out=27
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
