
import cv2
import numpy as np
import time
import serial
frameWidth = 640.0
frameHeight = 480.0
cap = cv2.VideoCapture(-1)
cap.set(3,frameWidth)
cap.set(4,frameHeight)
ser = serial.Serial(
        port='/dev/ttyS0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        xonxoff = False,     #disable software flow control
        rtscts = False ,    #disable hardware (RTS/CTS) flow control
        dsrdtr = False,       #disable hardware (DSR/DTR) flow control
        timeout=0)
Cx_T = 99999
Cx_C = 99999
Cx_R = 99999
Cy_T = 99999
Cy_R = 99999
Cy_C = 99999
angle1 = 0
angle2 = 0
angle3 = 0
while True:
    _, frame1 = cap.read()
    cameraMatrix = np.array([[5.403522780452443612e+02, 0.000000000000000000e+00, 3.133952019414790016e+02],
                         [0.000000000000000000e+00,5.393829989950471600e+02,2.850052639523698872e+02],
                         [0.000000000000000000e+00,0.000000000000000000e+00,1.000000000000000000e+00]])
    dist = np.array([[ 1.538463354087792889e-01,-1.977028622061018370e-01,5.866637732865324917e-03,7.024434555695516702e-04,-1.544848786530397117e-02
]])
    h,w = frame1.shape[:2]
    newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))
    frame = cv2.undistort(frame1, cameraMatrix, dist, None, newCameraMatrix)
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Every color except white
    low = np.array([0, 45, 51])
    high = np.array([121, 255, 255])
    mask = cv2.inRange(hsv_frame, low, high)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel)
    Contour,_ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in Contour:
        area = cv2.contourArea(cnt)
        if area > 10000:
            cv2.drawContours(frame,Contour,-1,(255,0,255),7)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)

            cv2.drawContours(frame,[box],0,(0,0,255),2)
            M =cv2.moments(cnt)
            Cx = int(M['m10']/M['m00'])
            Cy = int(M['m01']/M['m00'])

            cv2.circle(frame,(Cx,Cy),7,(255,255,255),-1)
            cv2.putText(frame,"("+str(-float(Cx/10))+" , " +str(-float(Cy/10))+")",(Cx-2,Cy -2),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,255,0),1)

            x,y,w,h = cv2.boundingRect(approx)
            if len(approx) != 3 and len(approx) != 4 and len(approx)!=8:
                cv2.putText(frame,"Unknown",(x+40,y -20),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,255,0),2)
                Cx_T = Cx_R = Cx_C = 99999
                Cy_T = Cy_R = Cy_C = 99999

            elif len(approx) == 3:
                cv2.putText(frame,"Triangle",(x+40,y -20),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,255,0),2)
                M_Triangle =cv2.moments(cnt)
                Cx_T = -round((M_Triangle['m10']/M_Triangle['m00'])/10,2)
                Cy_T = -round((M_Triangle['m01']/M_Triangle['m00'])/10,2)
                rect1 = cv2.minAreaRect(cnt)
                width = int(rect1[1][0])
                height = int(rect1[1][1])
                angle3 = int(rect1[2])
                label1 = " Angle of Triangle: " + str(-angle3) + " degrees"
                cv2.putText(frame, label1, (50,20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                if width < height:
                    angle3 = 90-angle3
                elif width > height:
                    angle3 = -angle3
                elif width == height:
                    angle3 = 90+angle3
                #angle3 = 90-int(rect1[2])
            elif len(approx) == 4:
                cv2.putText(frame,"Rectangle",(x+40,y -20),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,255,0),2)
                M_Rectangle =cv2.moments(cnt)
                Cx_R = -round((M_Rectangle['m10']/M_Rectangle['m00'])/10,2)
                Cy_R = -round((M_Rectangle['m01']/M_Rectangle['m00'])/10,2)
                rect2 = cv2.minAreaRect(cnt)
                width = int(rect2[1][0])
                height = int(rect2[1][1])
                angle1 = int(rect2[2])
                if width < height:
                    angle1 = 90-angle1
                elif width > height:
                    angle1 = -angle1
                elif width == height:
                    angle1 = 90+angle1
                label2 = " Angle of Rectangle: " + str(angle1) + " degrees"
                cv2.putText(frame, label2, (50,40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            elif len(approx) >= 8 and len(approx) <= 11 :
                cv2.putText(frame,"Circle",(x+40,y -20),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,255,0),2)
                M_Circle =cv2.moments(cnt)
                Cx_C = -round((M_Circle['m10']/M_Circle['m00'])/10,2)
                Cy_C = -round((M_Circle['m01']/M_Circle['m00'])/10,2)
                rect3 = cv2.minAreaRect(cnt)
                angle2 = 0
                label3 = " Angle of Circle: " + str(angle2) + " degrees"
                cv2.putText(frame, label3, (50,60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
    datasend = np.array([Cx_R,Cy_R,Cx_C,Cy_C,Cx_T,Cy_T,angle1,angle2,angle3])
    if ser.isOpen():
        ser.write("{},{},{},{},{},{},{},{},{}".format(*datasend).encode())
        print("Rectangle: {} {} ,circle: {} {},Triangle: {} {} and angle:{},{},{}\n".format(*datasend))
    cv2.imshow("contour", frame)
    #cv2.imshow("Result", result)

    key = cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()