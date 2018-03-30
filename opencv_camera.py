import time
import cv2
import numpy as numpy

class Camera(object) : #Populate a queue using Thread?
    def __init__(self) :
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.cv.CV_CAP_PROP_FPS, 60)
        self.camera.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1280) #1920)
        self.camera.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 720) #1080)

    def capture(self) :
        ret, frame = self.camera.read()
        return frame

    def capture_gray(self) :
        frame = self.capture()
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        return gray

    def stream_color(self) :
        ret, frame = self.camera.read() #bmp,jpeg
        ret, encoded = cv2.imencode('.jpg', frame)
        return encoded.tostring()

    def stream_gray(self) :
        frame = self.capture_gray()
        ret, encoded = cv2.imencode('.jpg', frame)
        return encoded.tostring()

