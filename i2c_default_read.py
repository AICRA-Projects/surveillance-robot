from flask import Flask, render_template, Response
from flask import Flask, render_template, request, redirect, url_for, make_response
import cv2
import smbus
import time
addr = 0x8
channel = 1
bus = smbus.SMBus(channel)
addr_rec = 0x9
def writenumber(val):
    bus.write_byte(addr,val)
    return -1
def stringtobyte(val):
    ret =[]
    for i in val:
        ret.append(ord(i))
    return ret

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
        video = cv2.VideoCapture(0)
        faceCascade = cv2.CascadeClassifier('/home/pi/Downloads/opencv-master/data/haarcascades/haarcascade_frontalface_default.xml')
        while True:
                try:
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
                    data = bus.read_byte(addr_rec)
                    print(data)
                    if data == 90:
                        in1 = 3
                        writenumber(in1)
                        time.sleep(0.05)
                        in1 = 11
                        writenumber(in1)
                    elif data == 80:
                        in1 = 5
                        writenumber(in1)
                    elif data == 70:
                        in1 = 3
                        writenumber(in1)
                    elif data == 50:
                        in1 = 10
                        writenumber(in1)
                    else:
                        in1 = 0
                        writenumber(in1)
                except OSError:
                    data = bus.read_byte(addr_rec)
                    print(data)
                except IOError:
                    data = bus.read_byte(addr_rec)
                    print(data)
        
                



    
@app.route("/face_feed")                                         
def face_feed():
    return Response(face(),
                mimetype='multipart/x-mixed-replace; boundary=fram')




@app.route('/manual.html')
def manual_mode():
    in3 = 2
    writenumber(in3)
    return render_template('man.html')

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

