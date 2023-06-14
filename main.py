from flask import Flask,render_template,Response
import numpy as np
import cv2

app = Flask(__name__,template_folder='template')

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
dim = (250,250)
font = cv2.FONT_HERSHEY_COMPLEX

def generate_frames():
   
   while True:
    success,frame = cap.read() #THIS IS AREA WITH BUG THAT is undetectable


    
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
                
                #if cv2.waitKey(1) & 0xFF == ord('t'):
                    cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)
                    cv2.putText(frame, "Triangle", (x, y), font, 1, (0, 0, 0))
                    
            elif len(approx) == 4:
                
                #if cv2.waitKey(1) & 0xFF == ord('r'):
                    cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)
                    cv2.putText(frame, "Rectangle", (x, y), font, 1, (0, 0, 0))
            elif circle is not None:
                circle = np.uint16(np.around(circle))[0,:]
                for j in circle:
                    #if cv2.waitKey(1) & 0xFF == ord('s'):
                        cv2.circle(frame, (j[0], j[1]), j[2], (0, 255, 0), 2)
                        x = circle.ravel()[0]
                        y = circle.ravel()[1]
                        cv2.putText(frame, "Circle", (x, y), font, 1, (0, 0, 0))

    if not success:
       break
    else:
       ret,buffer = cv2.imencode('.jpg',frame)
       frame = buffer.tobytes()

    yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    

@app.route("/")
def index():
    return render_template('index.html')



@app.route("/videos")
def videos():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')
    




    
                          


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
    


#cap.release()
#cv2.destroyAllWindows()