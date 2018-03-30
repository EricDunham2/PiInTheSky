from opencv_recorder import Recorder
import time
from threading import Thread
from opencv_software_detection import Motion_Handler

class Recording_Logic(Thread) :
    def __init__(self,_camera) :
        self.camera = _camera
        self.motion = Motion_Handler()
        self.recording = False
        self.is_motion = None
        self.rbuffer = None
        self.mbuffer = None

        Thread.__init__(self)

    def run(self) :
        try :
            self.motion.start()
            last_motion = time.time()

            while True:
                frame = self.camera.capture()
                time_delta = time.time() - last_motion

                self.mbuffer = self.motion.buffer_length
                self.is_motion = self.motion.get_motion_status()

                self.motion.add_frame(frame)

                if self.motion.get_motion_status() :

                    #if self.recorder :
                    #    self.rbuffer = len(self.recorder.buffer)
                    #else :
                    #    self.mbuffer = 0

                    last_motion = time.time()

                    if not self.recording :
                        print 'Recording started...'
                        self.recorder = Recorder()
                        self.recorder.start()
                        self.recording = True
                    elif self.recording :
                        self.recorder.buffer.append(frame)
                elif not self.motion.get_motion_status() :
                    if self.recording :
                        if time_delta > 30 :#Replace with a variable
                            self.recorder.stop()
                            print 'Recording stopped...'
                            self.recorder.join()
                            self.recording = False
                        else :
                            #print 'Adding frame...'
                            self.recorder.buffer.append(frame)
        except Exception as e :
            print 'Recording Logic: ' + str(e)
