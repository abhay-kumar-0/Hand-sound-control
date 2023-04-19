from unittest import result
import cv2
import mediapipe as mp
import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))




cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

while True:
    sucess,img=cap.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mplist=[]
            for id,lm in enumerate(handLms.landmark):
               # print(id,lm)
               h,w,c=img.shape
               cx,cy = int(lm.x*w) , int(lm.y*h)
               #print(id,cx,cy)
               mplist.append([id,cx,cy])
            if mplist:
               #print(mplist[4])
               x1,x2 = mplist[4][1], mplist[4][2]
               y1,y2 = mplist[8][1],mplist[8][2]
               
               cv2.circle(img,(x1,x2),10,(209,105,100),cv2.FILLED)
               cv2.circle(img,(y1,y2),10,(209,105,100),cv2.FILLED)
               cv2.line(img,(x1,x2),(y1,y2),(10,200,210),3)
               length = math.hypot((y1-x1),(y2-x2))
               #print(length)
               if length<30:
                z1=(x1+y1)//2
                z2=(x2+y2)//2 
                cv2.circle(img,(z1,z2),7,(10,200,150),cv2.FILLED) 
            volrange = volume.GetVolumeRange()
            minval = volrange[0]
            maxval = volrange[1]
            vol = np.interp(length,[25,200],[minval,maxval])
            volume.SetMasterVolumeLevel(vol, None)
            mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)
    cv2.imshow("image",img)
    cv2.waitKey(1)