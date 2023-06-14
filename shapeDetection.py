import cv2
import numpy as np



def nothing(x):
    # any operation
    pass

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)



font = cv2.FONT_HERSHEY_COMPLEX

while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    lower_color = np.array([0,0,168])
    upper_color = np.array([172,111,255])

    mask = cv2.inRange(hsv, lower_color, upper_color)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel)

   
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    

    for cnt in contours:
        area = cv2.contourArea(cnt)
        approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True) #approx the shape's contoour
        x = approx.ravel()[0]
        y = approx.ravel()[1]
        
        
        if area > 400:
            circle = cv2.HoughCircles(mask,cv2.HOUGH_GRADIENT,1,50,param1=50,param2=35, minRadius=0,maxRadius=0)

            if len(approx) == 3:
                
                if cv2.waitKey(1) & 0xFF == ord('t'):
                    cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)
                    cv2.putText(frame, "Triangle", (x, y), font, 1, (0, 0, 0))
                    
            elif len(approx) == 4:
                
                if cv2.waitKey(1) & 0xFF == ord('r'):
                    cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)
                    cv2.putText(frame, "Rectangle", (x, y), font, 1, (0, 0, 0))
            elif circle is not None:
                circle = np.uint16(np.around(circle))[0,:]
                for j in circle:
                    if cv2.waitKey(1) & 0xFF == ord('s'):
                        cv2.circle(frame, (j[0], j[1]), j[2], (0, 255, 0), 2)
                        x = circle.ravel()[0]
                        y = circle.ravel()[1]
                        cv2.putText(frame, "Circle", (x, y), font, 1, (0, 0, 0))
                        """
            elif 10 < len(approx) < 20:
                
                if cv2.waitKey(1) & 0xFF == ord('c'):
                    cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)
                    cv2.putText(frame, "Circle", (x, y), font, 1, (0, 0, 0))
            """


    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()