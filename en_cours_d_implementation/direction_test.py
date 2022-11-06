from direction import Direction
from time import sleep
from djitellopy import Tello

def drone_init():
    drone = Tello()
    drone.connect()
    print(f"Batterie: {drone.get_battery()}%")
    print(f"Temperature: {drone.get_temperature()}C")
    drone.streamoff()
    drone.streamon()
    sleep(2)
    drone.send_rc_control(0, 0, 0, 0)

    return drone

# drone = drone_init()
drone = None

cible = 0

direction = Direction(drone, None, True)
direction.import_mask_color(cible)

angle_hori, angle_vert, length, distance = direction.check_angles(cible)

print(f"\t\tangle_vert:{angle_vert}, angle_hori:{angle_hori}, length: {length}, distance: {distance}")
