import math
from time import sleep

class Travel:
    def __init__(self, drone, test:bool = False):
        self.drone = drone
        self.test = test
    
    # défini les composantes x et y en fontion des angles mesurés (fonction interne)
    @staticmethod
    def __find_target_position(angle_vert, angle_hori, distance):
        print(f"\t\ttangle_vert:{angle_vert}, angle_hori:{angle_hori}, distance: {distance}")
        if angle_hori > 90:
            angle = 180-angle_hori
        else:
            angle = angle_hori
        
        print(f"\t\tangle:{angle}")
        
        X_distance = math.cos(math.radians(angle))*distance
        Y_distance = math.sin(math.radians(angle))*distance
        
        if angle_hori < 90:
            if angle_vert < 90:
                print("\t\tcadran 1")
                pass
            else:
                print("\t\tcadran 2")
                Y_distance = -Y_distance
        else:
            if angle_vert < 90:
                X_distance = -X_distance
                print("\t\tcadran 4")
            else:
                X_distance = -X_distance
                Y_distance = -Y_distance
                print("\t\tcadran 3")
        
        print(f"\t\tx_distance:{X_distance}, y_distance:{Y_distance}")
                
        return X_distance, Y_distance


    # pour faire bouger le drone devant la cible
    def move_to_target(self, angle_hori, angle_vert, distance):
        x, y = self.__find_target_position(angle_vert, angle_hori, distance)
        
        x, y = round(x), round(y)

        self.speed = 1
        
        if not self.test:
            if x < 0 and y < 0:
                #bas gauche
                self.drone.go_xyz_speed(x, y, 0, self.speed)
                # self.drone.move_left(abs(x))
                # self.drone.move_down(abs(y))
            elif x < 0 and y > 0:
                #haut gauche
                self.drone.go_xyz_speed(x, y, 0, self.speed)
                # self.drone.move_left(abs(x))
                # self.drone.move_up(abs(y))
            elif x > 0 and y > 0:
                #haut droite
                self.drone.go_xyz_speed(x, y, 0, self.speed)
                # self.drone.move_right(abs(x))
                # self.drone.move_up(abs(y))
            elif x > 0 and y < 0:
                #bas droite
                self.drone.go_xyz_speed(x, y, 0, self.speed)
                # self.drone.move_right(abs(x))
                # self.drone.move_down(abs(y))

        if self.test:
            if x < 0 and y < 0:
                print(f"\t\tmove left: {abs(x)} and down: {abs(y)}")
            elif x < 0 and y > 0:
                print(f"\t\tmove left: {abs(x)} and up: {abs(y)}")
            elif x > 0 and y > 0:
                print(f"\t\tmove right: {abs(x)} and up: {abs(y)}")
            elif x > 0 and y < 0:
                print(f"\t\tmove right: {abs(x)} and down: {abs(y)}")

       #pour l'alignement         
    def lineup(self, status):
        if not self.test:
            if status == "left":
                self.drone.send_rc_control(-1, 0, 0, 0)
            elif status == "right":
                self.drone.send_rc_control(1, 0, 0, 0)
            elif status == "up":
                self.drone.send_rc_control(0, 0, -1, 0)
            elif status == "down":
                self.drone.send_rc_control(0, 0, 1, 0)
            else:
                self.drone.send_rc_control(0, 0, 0, 0)
        else:
            if status == "nothing":
                print("\t\taligned :)")