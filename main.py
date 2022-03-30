import cv2
import numpy as np
import utils
from djitellopy import Tello
from time import sleep

video = cv2.VideoCapture(0)

color_state = 0
color_sum = 2
tello = None 
test = False

cv2.namedWindow("trackbar")

def empty(x):
    pass

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

def drone():
    global tello
    tello = Tello()
    tello.connect()
    tello.streamoff()
    tello.streamon()

    print(f"Batterie: {tello.get_battery()}%")
    print(f"Temperature: {tello.get_highest_temperature(), tello.get_lowest_temperature()}C")

def main():
    global color_state
    global color_sum
    global tello
    
    colorchange()
    if not test:
        drone()

    while True:
        if test:
            _, img = video.read()
        elif not test:
            img = tello.get_frame_read()
        else:
            break

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
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
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
                    cv2.putText(img, str(round(angle)), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        cv2.imshow("mask", mask), cv2.imshow("image", img)
        
        if cv2.waitKey(1) & 0xFF == ord("q"):
            if color_state == color_sum:
                cv2.destroyAllWindows()
                break
            else:
                colorchange()
                print("sleeping 1s")
                sleep(1)

if __name__ == '__main__':
    main()