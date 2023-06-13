import numpy as np
import cv2


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
dim = (350,350)

while(True):
    ret, frame = cap.read()
    gray = cv2.medianBlur(cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY),5)
    resized = cv2.resize(gray,dim,interpolation = cv2.INTER_AREA)
    circle = cv2.HoughCircles(resized,cv2.HOUGH_GRADIENT,1,50,param1=50,param2=35, minRadius=0,maxRadius=0)
    if circle is not None:
        circle = np.uint16(np.around(circle))[0,:]
        for j in circle:
            if cv2.waitKey(1) & 0xFF == ord('s'):
                cv2.circle(resized, (j[0], j[1]), j[2], (0, 255, 0), 2)
                #cv2.putText(frame, 'cirlce', (j[0], j[1]),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_4)
        cv2.imshow('shape detector',resized)
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



    
                          
cap.release()
cv2.destroyAllWindows()