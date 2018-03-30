#Get the Streaming Frames
from opencv_camera import Camera
from threading import Thread
import time

class Stream(Thread) :
    def __init__(self) :
        self.camera = Camera()
        print 'Stream started...'
        Thread.__init__(self)

    def run(self) :
        global stream_frame
        while True :
            print 'Capping stream...'
            frame = self.camera.stream_color()
            yield stream_frame (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    
