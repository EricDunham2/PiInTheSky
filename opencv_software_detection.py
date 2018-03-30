from threading import Thread
from opencv_camera import Camera
from collections import deque
import numpy as np
import cv2
import time
#------------------------------------------------------------------#
#                   Detection/Recording Logic                      #
#------------------------------------------------------------------#

motion = False
buffer = []
motion_low = 1
motion_high = 0
stopped = False

class Motion_Handler(object) :
    def __init__(self) :
        global buffer
        buffer = []
        self.buffer_length = None

    def start(self) :
        tf = Thread_Foreman()
        tf.start()

    def stop(self) :
        global stopped
        stopped = True

    def get_motion_status(self) :
        return motion

    def add_frame(self,frame) :
        global buffer
        if len(buffer) < 100 :
            buffer.append(frame)
            self.buffer_length = len(buffer)

class Thread_Foreman(Thread) :
    def __init__(self) :
        self.thread_pool = []
        self.number_of_workers = 0
        self.threshold_low = 20
        self.threshold_high = 60
        Thread.__init__(self)

    def run(self) :
        time.sleep(2)

        self.hire()
        self.hire()
        self.hire()

        while not stopped :
            try :
                time.sleep(3)
                buffer_initial = len(buffer)
                time_initial = time.time()

                #print buffer_initial

                if len(buffer) > self.threshold_high :
                    self.hire()
                elif len(buffer) < self.threshold_low :
                    self.fire()
            except Exception as e :
                print 'Thread handler: ' +  str(e)

        self.declare_bankruptcy()

    def hire(self) :
        #print 'Hiring...'
        new_hire = Motion_Logic()
        self.thread_pool.append(new_hire)
        self.thread_pool[-1].start()
        self.number_of_workers += 1

    def fire(self) :
        if len(self.thread_pool) >= 2 :
            #print 'Firing...'
            self.thread_pool[-1].stop = True
            #print 'Joined'
            del self.thread_pool[-1]
            #print 'Deleted'
            self.number_of_workers -= 1

    def delcare_bankruptcy(self) :
        while len(buffer) != 0 :
           del self.thread_pool[-1]
        super(Thread_Foreman,self).join()


class Motion_Logic(Thread) :
    """Given image frames will detect whether motion has occurred"""
    def __init__(self) :
        self.delta_thresh = 5
        self.stop = False
        Thread.__init__(self)

    def run(self):
        while not stopped or self.stop :
            try :
                global buffer

                if motion :
                    #print 'High State...'
                    time.sleep(motion_high)
                else :
                    #print 'Low State'
                    time.sleep(motion_low)

                if len(buffer) > 10 :
                    frames = []
                    while len(frames) < 3 : # for x in range(0,3) :
                        try :
                            current_frame = cv2.cvtColor(buffer.pop(0),cv2.COLOR_BGR2GRAY)
                            frames.append(current_frame)
                        except ValueError :
                            pass
                    self.is_motion(frames)
            except Exception as e :
                print 'Motion Logic: ' + str(e)
        print 'Stopped...'

    def is_motion(self,frames) :

        if not frames :
            return

        f0 = frames[0]
        f1 = frames[1]
        f2 = frames[2]

        delta = []
        delta = self.diffImg(f0,f1,f2)

        if type(delta) is not np.ndarray or  not delta.any() :
            return

        self.map_contours(delta)


    def map_contours(self,delta) :
            global motion
            (cnts, _) = cv2.findContours(delta.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #Look up
            print 'Reading contours...'

            if len(cnts) == 0  or cnts == None:
                print 'No contours...'
                motion = False

            for c in cnts :
                print 'Contours found...'
                if cv2.contourArea(c) < 100 :
                    print 'Smaller than threshold...'
                    motion = False
                    continue
                print 'Larger than threshold...'
                motion = True
                break

    def diffImg(self,t0,t1,t2) :
        thresh = []

        d1 = cv2.absdiff(t2,t1)
        d2 = cv2.absdiff(t1,t0)
        d3 = cv2.bitwise_and(d1,d2)

        thresh = cv2.threshold(d3,5,255,cv2.THRESH_BINARY)[1]

        if type(thresh) is not np.ndarray or not thresh.any() :
            return None

        kernel = np.ones((5,5),np.uint8)
        eroded = cv2.erode(thresh,kernel,iterations = 1)
        return cv2.dilate(eroded,kernel,iterations = 1)
