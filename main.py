from djitellopy import Tello
import cv2
from two_points_angle_and_range_finder import direction

if __name__ == '__main__':
    cible = 0
    while True:
        direction.import_mask(cible)
        travel
        alignement
        travel
        cible += 1