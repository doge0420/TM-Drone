from djitellopy import Tello
import cv2

tello = Tello()
tello.connect()
tello.streamoff()
tello.streamon()
tello.takeoff()

print(f"Batterie: {tello.get_battery()}%")
print(f"Temperature: {tello.get_highest_temperature(), tello.get_lowest_temperature()}C")

def capture():
    frame = tello.get_frame_read()
    truc = True
    while truc:
        img = frame.frame
        cv2.imshow("frames", img)
        tello.send_rc_control(0,0,0,0)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            truc = False
            print("shutting down...")
            cv2.destroyAllWindows()
            tello.end()
            
capture()