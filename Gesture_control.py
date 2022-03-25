import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)
md = mp.solutions.hands
hands = md.Hands()
mpdraw = mp.solutions.drawing_utils
ctime = 0
ptime = 0
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = hands.process(gray)
    if res.multi_hand_landmarks:
        for hdl in res.multi_hand_landmarks:
            for id,lm in enumerate(hdl.landmark):
                h,w,c = frame.shape
                cx,cy =  int(lm.x*w) ,int(lm.y*h)
                print(id,cx,cy)
                if id == 10:
                    cv2.circle(frame,(cx,cy),25,(0,255,255),cv2.FILLED)


            mpdraw.draw_landmarks(frame,hdl,md.HAND_CONNECTIONS) 
    
    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime

    cv2.putText(frame,str(int(fps)),(10,50),cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,0),1)
    cv2.imshow("IMAGE",frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


