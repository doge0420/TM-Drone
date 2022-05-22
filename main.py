from djitellopy import Tello
import cv2
from direction import Direction
from travel import Travel
from alignement import Alignement

def main(drone, test:bool = False):
    cible = 0

    direction = Direction(drone)
    travel = Travel(drone)
    alignement = Alignement(drone, travel)

    while True:
        print(f"cible: {cible}")

        """direction"""
        
        print("Obtention de la direction...")
        direction.import_mask_color(cible)
        angle_hori, angle_vert, length, distance = direction.check_angles()

        """travel"""
        
        print("Déplacement vers la cible...")
        print(f"\tLongueur mesures: {length}")
        travel.move_to_target(angle_hori, angle_vert, distance)

        """alignement"""
        
        print("Alignement avec la cible...")
        alignement.import_mask_color(cible)
        alignement.align()

        """travel"""
        
        print("Passage à travers la cible...")

        cible += 1
        
        if cible == 2:
            break

    if not test:
        drone.end()

def drone_init():
    drone = Tello()
    drone.connect()
    drone.streamoff()
    drone.streamon()
    drone.send_rc_control(0, 0, 0, 0)
    drone.set_speed(0)
    
    print(f"Batterie: {drone.get_battery()}%")
    print(f"Temperature: {drone.get_highest_temperature(), drone.get_lowest_temperature()}C")  
    
    return drone

if __name__ == '__main__':
    drone = drone_init()
    main(drone)