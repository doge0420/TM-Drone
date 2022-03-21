import cv2
import numpy as np

video = cv2.VideoCapture(0)

def track(x):
    pass

cv2.namedWindow("trackbar")
cv2.createTrackbar("low_h", "trackbar", 0, 180, track)
cv2.createTrackbar("low_s", "trackbar", 0, 255, track)
cv2.createTrackbar("low_v", "trackbar", 0, 255, track)
cv2.createTrackbar("hi_h", "trackbar", 180, 180, track)
cv2.createTrackbar("hi_s", "trackbar", 255, 255, track)
cv2.createTrackbar("hi_v", "trackbar", 255, 255, track)

while True:
    success, img = video.read()
    image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    low_h = cv2.getTrackbarPos("low_h", "trackbar")
    low_s = cv2.getTrackbarPos("low_s", "trackbar")
    low_v = cv2.getTrackbarPos("low_v", "trackbar")
    hi_h = cv2.getTrackbarPos("hi_h", "trackbar")
    hi_s = cv2.getTrackbarPos("hi_s", "trackbar")
    hi_v = cv2.getTrackbarPos("hi_v", "trackbar")
    
    lower = np.array([low_h, low_s, low_v])
    upper = np.array([hi_h, hi_s, hi_v])
    
    mask = cv2.inRange(image, lower, upper)
    
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) != 0:
        for contour in contours:
            if cv2.contourArea(contour) > 300:      #pixels
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255), 3)
                # print(f"position:{x,y}")
    
    cv2.imshow("mask", mask), cv2.imshow("image", img)
    
    
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break