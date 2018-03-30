from flask import Flask, render_template, redirect, request, url_for, Response
import flask_login #as flask_login
from flask_login import LoginManager, UserMixin
from flask_socketio import SocketIO
import time
import json
import logging
from logging.handlers import RotatingFileHandler
from threading import Thread
from system_monitor import Monitor
from opencv_camera import Camera
#from opencv_software_detection import MotionCapture
#from opencv_recorder import Recorder
from terminal import Terminal
from streaming_motion_logic import Recording_Logic
#Decouple the recording from the motion detection


login_manager = LoginManager()

app = Flask(__name__)
app.secret_key = 'key'

login_manager.init_app(app)
socketio = SocketIO(app)
connected = True
terminal = Terminal(False)
camera = Camera()
monitor = Monitor() 
users = {'json':{'pw':'pass'}}  #Get from the database
stream_frame = None
thread = None

@socketio.on('connect', namespace='/protected')
def set_connected() :
    global connected
    connected = True

@socketio.on('disconnect', namespace='/protected')
def set_disconnected() :
    global connected
    connected = False

class User(UserMixin): #What is this for
    pass

@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return

    user = User()
    user.id = username
    return user

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username','placeholder')

    user = User()
    user.id = username
    if username not in users :
        return

    user.is_authenticated = request.form['pw'] == users[username]['pw']
    return user

def gen():
    global camera
    global stream_frame

    while connected :
        try :
            frame = camera.stream_color()
            resp = (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            stream_frame = resp
        except ValueError :
            pass

def get_frame() :
    while True :
        while not stream_frame :
            time.sleep(.3)
        yield stream_frame


@app.route('/video_feed')
@flask_login.login_required
def video_feed():
    global thread
    if thread == None :
        thread = Thread(target = gen)
        thread.start()

    return Response(get_frame(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/system_stats', methods=['GET'])
@flask_login.login_required
def stats():
    try :
        return json.dumps({'temp':monitor.temp,'memory':monitor.memory,'dspeed':monitor.dspeed,'uspeed':monitor.uspeed,'space':monitor.space,'mbuffer':motion.mbuffer,'rbuffer':motion.rbuffer,'is_motion':motion.is_motion})
    except ValueError :
        return ValueError

@app.route('/exe', methods=['POST'])
@flask_login.login_required
def execute():
    global terminal
    #return 'Unlimited Power!\r\nThis feature was removed do to a terrifying realization that it was a cool yet, but horrible mistake'
    #cmd = request.json['cmd']
    #return terminal.execute(cmd)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')

        if request.form.get('pw','placeholder') == users[username]['pw'] :
            user = User()
            user.id = username
            flask_login.login_user(user)
            return redirect(url_for('protect'))
    return render_template("index.html")

@app.route('/stream')
@flask_login.login_required
def protect():
    if not monitor.is_alive() :
        monitor.start()

    return render_template('protected.html')

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

if __name__ == '__main__':
    #app.debug = True
    app.threaded = True
    file_handler = RotatingFileHandler('python.log', maxBytes=1024 * 1024 * 100, backupCount=20)
    file_handler.setLevel(logging.ERROR)
    print 'Starting'
    motion = Recording_Logic(camera)
    motion.start()

    app.logger.addHandler(file_handler)

    app.config['TRAP_BAD_REQUEST_ERRORS'] = True
    socketio.run(app,host="0.0.0.0")

