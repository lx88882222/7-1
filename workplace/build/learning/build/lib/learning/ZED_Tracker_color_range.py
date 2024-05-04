import cv2
import numpy as np
import sys
 
def nothing(x):
    pass

def main():
    video = cv2.VideoCapture("/home/mi/Videos/test1.mp4")
    
    if not video.isOpened():
        print("fail to open mp4 file")
        sys.exit()

    cv2.namedWindow("Trackbars")
 
    cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing) 
    cv2.createTrackbar("L - S", "Trackbars", 0, 155, nothing)
    cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("U - H", "Trackbars", 0, 179, nothing)  #179
    cv2.createTrackbar("U - S", "Trackbars", 0, 255, nothing) #255
    cv2.createTrackbar("U - V", "Trackbars", 0, 255, nothing) #255
 
    while True:
        # Read a new frame
        ret, frame = video.read()

        if not ret:
            break
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
        l_h = cv2.getTrackbarPos("L - H", "Trackbars")
        l_s = cv2.getTrackbarPos("L - S", "Trackbars")
        l_v = cv2.getTrackbarPos("L - V", "Trackbars")
        u_h = cv2.getTrackbarPos("U - H", "Trackbars")
        u_s = cv2.getTrackbarPos("U - S", "Trackbars")
        u_v = cv2.getTrackbarPos("U - V", "Trackbars")
 
        lower_blue = np.array([l_h, l_s, l_v])  #0, 156, 126
        upper_blue = np.array([u_h, u_s, u_v])  # 79, 255, 255
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
 
        result = cv2.bitwise_and(frame, frame, mask=mask)
 
        cv2.imshow("frame", frame)
        cv2.imshow("mask", mask)
        cv2.imshow("result", result)
 
        key = cv2.waitKey(30)
        if key == 27:
            break
 

    cv2.destroyAllWindows()
