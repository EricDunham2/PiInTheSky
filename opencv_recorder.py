import uuid
import cv2
from threading import Thread
from collections import deque
#from sftp_transfer import SFTP
from system_monitor import Monitor
import time

class Recorder(Thread) :
    def __init__(self, conf=None) :
        self.output = None
        self.stopped = False
        self.fourcc = cv2.cv.CV_FOURCC('X','V','I','D')
        self.uid = None
        self.framerate = 30
        self.resolution =  (1280,720) #(1920,1080)
        self.extension = '.avi'
        self.localpath = '/home/pi/Documents/'
        self.buffer = deque(maxlen=100)
        self.frame_count = 0
        self.monitor = Monitor()
        self.sftp_host = '192.168.2.1'
        self.sftp_port = 22
        self.sftp_password = 'pass'
        self.sftp_username = 'pi'
        self.memory_threshold = 500
        Thread.__init__(self)

    def run (self) :
        self.create_file()
        self.monitor = Monitor()
        self.monitor.start()
        while not self.stopped and self.output:
            try :
                #print len(self.buffer)
                #print self.monitor.memory
                #if self.monitor.memory > self.memory_threshold :
                    #print str(self.monitor.memory) + str(self.memory_threshold)
                    #print 'MEM Threshhold reached...'
                    #time.sleep(10)
                    #self.save_file()
                    #self.create_file()

                if self.buffer :
                    #print 'Recording buffer size: ' + str(self.buffer)
                    self.record_frame(self.buffer.pop())
            except Exception as e:
                print 'Error in recorder...' + str(e)

    def create_file(self) :
        if self.output :
            return

        self.uid = str(uuid.uuid4())
        print self.uid
        self.output = cv2.VideoWriter(self.localpath + self.uid + self.extension, self.fourcc, self.framerate, tuple(self.resolution))

    def record_frame(self,frame) :
        if self.output :
            #print 'Recording frame...'
            self.frame_count = self.frame_count + 1
            self.output.write(frame)
            #print 'Frame recorded...'

    def save_file(self) :
        print 'Saving File...'
        localpath = '/home/pi/Documents/' + self.uid + self.extension
        remotepath = '/home/pi/Documents/' + self.uid + self.extension

        #ftp = SFTP(self.sftp_host,self.sftp_port,self.sftp_password,self.sftp_username,localpath,remotepath)
        #ftp.start()

        #self.output.release()
        print 'File Saved...'

    def stop(self) :
        print 'Stopping...'
        self.stopped = True
        #while self.buffer :
        #    self.record_frame(self.buffer.pop())
        self.save_file()
        print 'Captured ' + str(self.frame_count) + ' frames...'
        super(Recorder,self).join()
