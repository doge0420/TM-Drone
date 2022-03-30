import cv2
import numpy as np
import utils

video = cv2.VideoCapture(0)

color_state = 0
color_sum = 2

def empty(x):
    pass

cv2.namedWindow("trackbar")

# cv2.createTrackbar("low_h", "trackbar", 0, 180, empty)    #par defaut
# cv2.createTrackbar("low_s", "trackbar", 0, 255, empty)
# cv2.createTrackbar("low_v", "trackbar", 0, 255, empty)
# cv2.createTrackbar("hi_h", "trackbar", 180, 180, empty)
# cv2.createTrackbar("hi_s", "trackbar", 255, 255, empty)
# cv2.createTrackbar("hi_v", "trackbar", 255, 255, empty)

def colorchange():
    global color_state
    
    if color_state == 0:
        cv2.createTrackbar("low_h", "trackbar", 110, 180, empty)    #pour detecter le bleu
        cv2.createTrackbar("low_s", "trackbar", 150, 255, empty)
        cv2.createTrackbar("low_v", "trackbar", 20, 255, empty)
        cv2.createTrackbar("hi_h", "trackbar", 130, 180, empty)
        cv2.createTrackbar("hi_s", "trackbar", 255, 255, empty)
        cv2.createTrackbar("hi_v", "trackbar", 255, 255, empty)
        
        print("bleu")
        color_state += 1
        
    elif color_state == 1:
        cv2.createTrackbar("low_h", "trackbar", 0, 180, empty)    #rouge
        cv2.createTrackbar("low_s", "trackbar", 151, 255, empty)
        cv2.createTrackbar("low_v", "trackbar", 114, 255, empty)
        cv2.createTrackbar("hi_h", "trackbar", 10, 180, empty)
        cv2.createTrackbar("hi_s", "trackbar", 227, 255, empty)
        cv2.createTrackbar("hi_v", "trackbar", 255, 255, empty)
        
        print("rouge")
        color_state += 1

def main():
    global color_state
    global color_sum
    
    colorchange()
    
    while True:
        _, img = video.read()
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
                if cv2.contourArea(contour) > 350:
                    rect = cv2.minAreaRect(contour)
                    angle = rect[2]
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    
                    x, y = utils.getcenter(box)
                    start, end = utils.getmid(box)
                    
                    cv2.line(img, start, end, (0, 255, 0), 3)
                    cv2.drawContours(img, [box], 0, (0,0,255), 2)
                    cv2.circle(img, (x, y), radius=5, color=(0,255,0), thickness=-1)
                    cv2.putText(img, str(round(angle)), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)

        cv2.imshow("mask", mask), cv2.imshow("image", img)
        
        if cv2.waitKey(1) & 0xFF == ord("q"):
            if color_state == color_sum:
                cv2.destroyAllWindows()
                break
            else:
                colorchange()

if __name__ == '__main__':
    main()