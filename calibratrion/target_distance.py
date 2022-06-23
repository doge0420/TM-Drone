import cv2
from mask_window import Color_window
import numpy as np
from djitellopy import Tello
from threading import Thread

def win_run():
    global window
    window = Color_window()
    window.run()

t = Thread(target=win_run, daemon=True)
t.start()

drone = Tello()
drone.connect()
drone.streamon()
# drone.turn_motor_on()
print(f"Batterie: {drone.get_battery()}%")
print(f"Temperature: {drone.get_temperature()}C")  

video = drone.get_frame_read()

while True:
    img = video.frame
    img = cv2.resize(img, (640, 480))
    image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    blur = cv2.GaussianBlur(image, (5,5), 0)
    mask = window.get_mask(blur)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) != 0:
        for contour in contours:
            if cv2.contourArea(contour) > 350:
                rect = cv2.minAreaRect(contour)
                area = cv2.contourArea(contour)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
                print(f"\t {area}")
                print((15568*(area ** -0.496))+20)

    cv2.imshow("mask", mask), cv2.imshow("image", img)

    if cv2.waitKey(1) & 0xFF == ord("q") or window.get_status() == False:
        cv2.destroyAllWindows()
        drone.end()
        t.join()
        break