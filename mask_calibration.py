import cv2
import numpy as np
from threading import Thread
from mask_window import Color_window
from djitellopy import Tello
from time import sleep

def win_run():
    global window
    window = Color_window()
    window.run()

def main(test):
    global window

    t = Thread(target=win_run, daemon=True)
    t.start()
 
    if not test:
        drone = Tello()
        drone.connect()
        drone.streamon()
        drone.send_rc_control(0, 0, 0, 0)
        print(f"Batterie: {drone.get_battery()}%")
        print(f"Temperature: {drone.get_temperature()}C")  

        video = drone.get_frame_read()
        sleep(3)
    else:
        video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
 
    while True:
        if not test:
            img = video.frame
            img = cv2.resize(img, (640, 480))
        else:
            _, img = video.read()
            
        image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = window.get_mask(image)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) != 0:
            for contour in contours:
                if cv2.contourArea(contour) > 350:
                    rect = cv2.minAreaRect(contour)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    cv2.drawContours(img, [box], 0, (0, 0, 255), 2)

        cv2.imshow("mask", mask), cv2.imshow("image", img)

        if cv2.waitKey(1) & 0xFF == ord("q") or window.get_status() == False:
            cv2.destroyAllWindows()
            t.join()
            break

if __name__ == '__main__':
    main(test=True)