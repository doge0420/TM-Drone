from djitellopy import Tello
import cv2
from direction import Direction
from travel import Travel
from alignement import Alignement

def main(video, drone):
    cible = 0

    direction = Direction(video)
    travel = Travel(drone)
    alignement = Alignement(video)

    while True:
        print(f"cible: {cible}")

        #direction
        print("Obtention de la direction...")
        direction.import_mask_color(cible)
        angle_hori, angle_vert, length, distance = direction.check_angles()

        #travel
        print("Déplacement vers la cible...")
        print(f"Longueur mesures: {length}")
        travel.move_to_target(angle_hori, angle_vert, distance)

        # alignement
        print("Alignement avec la cible...")
        alignement.import_mask_color(cible)
        alignement.align()

        # travel
        print("Passage à travers la cible...")

        cible += 1
        
        if cible == 1:
            break

if __name__ == '__main__':
    video = cv2.VideoCapture(0)
    drone = Tello()
    
    main(video, drone)