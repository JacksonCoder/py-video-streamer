import camera
import cv2
from time import sleep

c = camera.CameraProcessor(0)
c.start_read()
while not camera.camera_open:
    sleep(0.1)
sleep(1)
f = c.get_latest()
cv2.imwrite("/home/jacksoncoder/cv2.jpg",f)
sleep(2)
c.close()