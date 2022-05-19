from djitellopy import Tello
import cv2
from direction import Direction
from travel import Travel
from alignement import Alignement
from track_window import Track_window

def win_run():
    global window
    window = Track_window()
    window.run()

def main():
    cible = 0
    win_run()

    while True:
        Track_window.update_current_step(cible)

        Track_window.update_status("Checking target position...")
        Direction.import_mask_color(cible)

        Track_window.update_status("Traveling to the next target...")
        angle_hori, angle_vert, length, distance = Direction.check_angles()
        print(length)
        Travel.move_to_target(angle_hori, angle_vert, distance)

        Track_window.update_status("Alignment with the target...")
        alignement

        Track_window.update_status("Passing through the target...")
        travel

        cible += 1

if __name__ == '__main__':
    main()