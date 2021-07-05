from flask import Flask, render_template, Response
from flask import Flask, render_template, request, redirect, url_for, make_response
import cv2
import smbus
import time
addr = 0x8
channel = 1
bus = smbus.SMBus(channel)

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


if __name__== '__main__':
    app.run(host='0.0.0.0',threaded=True)