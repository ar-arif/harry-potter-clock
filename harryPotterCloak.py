import requests
import cv2
import numpy as np
import time

url = "http://192.168.0.102:8080/shot.jpg"
def img():
    img_res = requests.get(url)
    img_arr = np.array(bytearray(img_res.content),dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)
    img = cv2.flip(img, 1)
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    img = cv2.resize(img, (280,300))
    return img

def background():
    img_res = requests.get(url)
    img_arr = np.array(bytearray(img_res.content),dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)
    img = cv2.flip(img, 1)
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    img = cv2.resize(img, (280,300))
    return img

for i in range(60):
	bg = background()
backg = bg

while True:
    hsv = cv2.cvtColor(img(), cv2.COLOR_RGB2HSV)
    lower_red = np.array([0,120,50])
    upper_red = np.array([10,255,255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    lower_red = np.array([170,120,70])
    upper_red = np.array([180,255,255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)
    mask1 = mask1+mask2
    mask1=cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
    mask1=cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3,3),np.uint8))
    mask2=cv2.bitwise_not(mask1)
    res1=cv2.bitwise_and(img(), img(), mask=mask2)
    res2=cv2.bitwise_and(backg, backg, mask=mask1)

    final=cv2.addWeighted(res1, 1, res2, 1, 0)
    cv2.imshow("Cloak", final)
    if cv2.waitKey(10)==ord('c'):
    	break