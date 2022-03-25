import cv2
import time
import numpy as np
import tracking_module as tm
import math


cap = cv2.VideoCapture(0)
detector = tm.hand_detector(detect = 0.7)
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volrange =volume.GetVolumeRange()

minvol = volrange[0]
maxvol = volrange[1]
vol = 0


ptime = 0

while True:
    ret,frame = cap.read()
    frame = detector.findhand(frame)
    lmlist = detector.findposition(frame,draw = False)
    if len(lmlist)!=0:
        x1,y1 = lmlist[4][1],lmlist[4][2]
        x,y = lmlist[8][1],lmlist[8][2]
        cx,cy = (x1+x) // 2 ,(y1 + y)//2
        cv2.circle(frame,(x1,y1),25,(0,255,255),cv2.FILLED)
        cv2.circle(frame,(x,y),25,(0,255,255),cv2.FILLED)
        cv2.line(frame,(x1,y1),(x,y),(255,0,0),3)
        cv2.circle(frame,(cx,cy),25,(0,255,255),cv2.FILLED)
        length = math.hypot(x - x1 , y - y1)
        vol = np.interp(length,[50,300],[minvol,maxvol])
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)
        if length < 50:
            cv2.circle(frame,(cx,cy),25,(255,255,255),cv2.FILLED)

    
    ctime = time.time()
    fps =1/(ctime-ptime)
    ptime = ctime
    cv2.putText(frame,str(int(fps)),(10,50),cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,0),1)

    cv2.imshow("IMAGE",frame)
    if cv2.waitKey(1) == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()