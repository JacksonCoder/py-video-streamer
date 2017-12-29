# Camera processing unit. Based on the SOBE camera module: https://github.com/SouthEugeneRoboticsTeam/SOBE/blob/single-image/camera.py
# Made by Jackson Lewis
# Oh, did I mention this runs in a seperate thread?

import threading
import cv2
lock = threading.Lock()
camera_open = False # Check if camera is on
close = False # Set to true to make the camera close
def read_loop(port,camera_state): # camera_state should be CameraProcessor
    global camera_open,close
    vc = cv2.VideoCapture(port)
    while not close:
        _,f = vc.read()
        if not camera_open: camera_open = True
        #
        # Put some code here later to setup 1080p resolution
        #
        lock.acquire()
        camera_state.frame = f
        lock.release()

class CameraProcessor:
    def __init__(self,port):
        self.camport = port
        self.frame = None

    def start_read(self):
        self.process = threading.Thread(target=read_loop,args=(self.camport,self))
        self.process.start()
    def get_latest(self):
        return self.frame
    def close(self):
        global close
        close = True

def is_on():
return camera_open
