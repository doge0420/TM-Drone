from djitellopy import Tello
from time import sleep


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
