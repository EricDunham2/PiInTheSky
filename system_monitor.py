import subprocess,psutil,os
from threading import Thread
import time 
from collections import deque

class Monitor(Thread) :
    def __init__(self) :
        self.temp_call = ['/opt/vc/bin/vcgencmd', 'measure_temp']
        Thread.__init__(self)

        self.temp = None
        self.uspeed = None
        self.dspeed = None
        self.space = None
        self.memory = None

    def run(self) :
        while True :
            try :
                self.temp = self.get_temperature()
                self.space = self.get_space()
                self.memory = self.get_memory()
                nspeed = self.get_network_speed()
                self.uspeed = nspeed[0]
                self.dspeed = nspeed[1]
                time.sleep(3) 
            except Exception as e :
                print str(e)

    def get_temperature(self) :
        temp  = subprocess.check_output(self.temp_call)
        return temp[5:]

    def get_space(self) :
        return str(round(psutil.disk_usage('/').used / 1024 / 1024 / 1024,2)) + ' Gb'

    def get_memory(self) :
        return str(psutil.virtual_memory().used >> 20)  +' Mb'

    def get_network_speed(self, dt=3, interface='wlan0'):
       counter = psutil.net_io_counters(pernic=True)[interface]
       tot = (counter.bytes_sent, counter.bytes_recv)
       t0 = time.time()

       last_tot = tot
       time.sleep(dt)
       counter = psutil.net_io_counters(pernic=True)[interface]
       t1 = time.time()
       tot = (counter.bytes_sent, counter.bytes_recv)
       ul, dl = [(now - last) / (t1 - t0) / 1000.0 for now, last in zip(tot, last_tot)]
       ul = str(round(ul,2)) + ' Kb/s'
       dl = str(round(dl,2)) + ' Kb/s'
       return (ul,dl)
