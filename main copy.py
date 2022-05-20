from djitellopy import Tello
import cv2
from threading import Thread
from direction import Direction
from travel import Travel
from alignement import Alignement
from track_window import Track_window

def win_run():
    global track_window
    track_window = Track_window()
    track_window.run()

def main():
    global track_window
    cible = 0

    t = Thread(target=win_run)
    t.start()


    while True:
        Track_window.update_current_step(track_window, cible)

        #direction
        Track_window.update_status(track_window, "Checking target position...")
        # Direction.import_mask_color(cible)

        # #travel
        # Track_window.update_status(track_window, "Traveling to the next target...")
        # angle_hori, angle_vert, length, distance = Direction.check_angles()
        # print(length)
        # Travel.move_to_target(angle_hori, angle_vert, distance)

        # # alignement
        # Track_window.update_status(track_window, "Alignment with the target...")

        # # travel
        # Track_window.update_status(track_window, "Passing through the target...")

        cible += 1
        if cible == 5:
            break
    t.join()

if __name__ == '__main__':
    main()