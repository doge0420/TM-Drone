import math

class Travel:
    def __init__(self, drone):
        self.drone = drone
    
    # défini les composantes x et y en fontion des angles mesurés (fonction interne)
    @staticmethod
    def __find_target_position(angle_vert, angle_hori, distance):
        print(f"\tangle_vert:{angle_vert}, angle_hori:{angle_hori}, distance: {distance}")
        if angle_hori > 90:
            angle = 180-angle_hori
            print(f"\tangle:{angle}")
        else:
            angle = angle_hori
            print(f"\tangle:{angle}")
        
        
        X_distance = math.cos(math.radians(angle))*distance
        Y_distance = math.sin(math.radians(angle))*distance
        
        if angle_hori < 90:
            if angle_vert < 90:
                print("\tcadran 1")
                pass
            else:
                print("\tcadran 2")
                Y_distance = -Y_distance
        else:
            if angle_vert < 90:
                X_distance = -X_distance
                print("\tcadran 4")
            else:
                X_distance = -X_distance
                Y_distance = -Y_distance
                print("\tcadran 3")
        
        print(f"\tx_distance:{X_distance}, y_distance:{Y_distance}")
                
                
        return X_distance, Y_distance
            
    # pour faire bouger le drone devant la cible
    def move_to_target(self, angle_hori, angle_vert, distance):
        x, y = self.__find_target_position(angle_vert, angle_hori, distance)
        
        x, y = round(x), round(y)
        
        if x < 0 and y < 0:
            print(f"left: {abs(x)}")
            print(f"down: {abs(y)}")
            # self.drone.move_left(abs(x))
            # self.drone.move_down(abs(y))
        elif x < 0 and y > 0:
            print(f"left: {abs(x)}")
            print(f"up: {abs(y)}")    
            # self.drone.move_left(abs(x))
            # self.drone.move_up(abs(y))
        elif x > 0 and y > 0:
            print(f"right: {abs(x)}")
            print(f"up: {abs(y)}")
            # self.drone.move_right(abs(x))
            # self.drone.move_up(abs(y))
        elif x > 0 and y < 0:
            print(f"right: {abs(x)}")
            print(f"down: {abs(y)}")
            # self.drone.move_right(abs(x))
            # self.drone.move_down(abs(y))