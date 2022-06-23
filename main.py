from djitellopy import Tello
import cv2
from direction import Direction
from travel import Travel
from alignement import Alignement
import utils
from time import sleep

def main(test: bool = False):
    cible = 0

    if not test:
        drone = drone_init()
    else:
        drone = None

    travel = Travel(drone, test)
    direction = Direction(drone, travel, test)
    alignement = Alignement(drone, travel, test)

    while True:
        print(f"--cible: {cible}--")

        """direction"""

        print("\tObtention de la direction...")
        direction.import_mask_color(cible)
        angle_hori, angle_vert, length, distance = direction.check_angles(
            cible)
        fromtarget, totarget = utils.import_mask_color(
            cible)[0]["name"], utils.import_mask_color(cible)[1]["name"]
        print(f"\t\t{fromtarget} --> {totarget}")

        """travel"""

        print("\n\tDéplacement vers la cible...")
        print(f"\t\tNombres mesures: {length}")
        travel.move_to_target(angle_hori, angle_vert, distance)

        """alignement"""

        print("\n\tAlignement avec la cible...")
        alignement.import_mask_color(cible)
        alignement.align()

        """travel"""

        print("\n\tPassage à travers la cible...")
        sleep(1)

        print(f"\n\t\t\t ######  Cible {cible} traversée :)  ######")
        cible += 1

        if cible == 1:
            print(f"Parcours terminé! Le drone a traversé les {cible} cibles")
            break

    if not test:
        drone.end()

def drone_init():
    drone = Tello()
    drone.connect()
    print(f"Batterie: {drone.get_battery()}%")
    print(f"Temperature: {drone.get_temperature()}C")
    drone.streamoff()
    drone.streamon()
    drone.takeoff()
    sleep(2)
    drone.send_rc_control(0, 0, 0, 0)

    return drone

if __name__ == '__main__':
    main(test = True)