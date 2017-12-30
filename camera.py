# Camera processing unit. Based on the SOBE camera module: https://github.com/SouthEugeneRoboticsTeam/SOBE/blob/single-image/camera.py
# Made by Jackson Lewis
# Oh, did I mention this runs in a seperate thread?

import threading
import cv2
lock = threading.Lock()
camera_open = False # Check if camera is on
frames = 0
close = False # Set to true to make the camera close
def read_loop(port,camera_state): # camera_state should be CameraProcessor
    global camera_open,close,frames
    vc = cv2.VideoCapture(port)
    # Set up some things (1080p res)
    vc.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    vc.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

    while not close:
        _,f = vc.read()
        frames += 1
        if not camera_open: camera_open = True
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
