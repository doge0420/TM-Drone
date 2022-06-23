import math

class Travel:
    def __init__(self, drone, test:bool = False):
        self.drone = drone
        self.test = test
        self.essai = 0
        self.speed = 10
    
    # défini les composantes x et y en fontion des angles mesurés (fonction interne)
    @staticmethod
    def __find_target_position(angle_vert, angle_hori, distance):
        print(f"\t\tangle_vert:{angle_vert}, angle_hori:{angle_hori}, distance: {distance}")
        if angle_hori > 90:
            angle = 180-angle_hori
        else:
            angle = angle_hori
        
        print(f"\t\tangle:{angle}")
        
        X_distance = math.cos(math.radians(angle))*distance * 10
        Y_distance = math.sin(math.radians(angle))*distance * 10
        
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
        
        if not self.test:
            self.drone.go_xyz_speed(0, -x, y, self.speed)
            
        if self.test:
            if x < 0 and y < 0:
                print(f"\t\tmove left: {abs(x)} and down: {abs(y)}")
            elif x < 0 and y > 0:
                print(f"\t\tmove left: {abs(x)} and up: {abs(y)}")
            elif x > 0 and y > 0:
                print(f"\t\tmove right: {abs(x)} and up: {abs(y)}")
            elif x > 0 and y < 0:
                print(f"\t\tmove right: {abs(x)} and down: {abs(y)}")

    # pour l'alignement         
    def lineup(self, status):
        if not self.test:
            if status == "left":
                self.drone.send_rc_control(-13, 0, 0, 0)
            elif status == "right":
                self.drone.send_rc_control(13, 0, 0, 0)
            elif status == "up":
                self.drone.send_rc_control(0, 0, 13, 0)
            elif status == "down":
                self.drone.send_rc_control(0, 0, -13, 0)
            else:
                self.drone.send_rc_control(0, 0, 0, 0)
        else:
            if status == "nothing":
                print("\t\taligned :)")
                
    def search(self):
        rayon = 50

        if self.essai == 0:
            self.drone.go_xyz_speed(0, rayon, 0, self.speed)
        elif self.essai == 1:
            self.drone.go_xyz_speed(0, -rayon, rayon, self.speed)
        elif self.essai == 2:
            self.drone.go_xyz_speed(0, -rayon, -rayon, self.speed)
        elif self.essai == 3:
            self.drone.go_xyz_speed(0, rayon, -rayon, self.speed)
        else:
            pass
        
        self.essai += 1
        
        if self.essai > 3:
            self.drone.land()
        
        return self.essai

    def go_to_target(self, area):
        area = ((15568*area) ** (-0.496))+20
        self.drone.move_forward(area)