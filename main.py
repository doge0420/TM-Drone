from djitellopy import Tello
from time import sleep
import cv2
from threading import Thread
import sys

tello = Tello()
tello.connect()
tello.streamoff()
tello.streamon()

print(f"Batterie: {tello.get_battery()}%")
print(f"Temperature: {tello.get_highest_temperature(), tello.get_lowest_temperature()}C")

frame = tello.get_frame_read()

def capture():
    truc = True
    while truc:
        img = frame.frame
        cv2.imshow("frames", img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            truc = False
            print("shutting down...")
            cv2.destroyAllWindows()
            tello.end()

window = Thread(target=capture)
window.start()

tello.takeoff()
tello.move_up(20)

window.join()