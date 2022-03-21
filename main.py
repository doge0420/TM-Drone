from time import sleep
from threading import Thread
import sys
import drone

if __name__ == '__main__':
    window = Thread(target=drone.capture)
    window.start()

    tello.takeoff()
    tello.move_up(20)

    window.join()