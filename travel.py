from math import sin, cos

class Travel:
    def __init__(self, drone):
        self.drone = drone
    
    # défini les composantes x et y en fontion des angles mesurés (fonction interne)
    @staticmethod
    def __find_target_position(angle_vert, angle_hori, distance):
        if angle_hori > 90:
            angle = 180-angle_hori
        
        X_distance = sin(angle)*distance
        Y_distance = cos(angle)*distance
        
        if angle_hori < 90:
            if angle_vert < 90:
                pass
            else:
                Y_distance = -Y_distance
        else:
            if angle_vert < 90:
                X_distance = -X_distance
            else:
                X_distance = -X_distance
                Y_distance = -Y_distance
                
        return X_distance, Y_distance
            
    # pour faire bouger le drone devant la cible
    def move_to_target(self, angle_vert, angle_hori, distance):
        x, y = self.__find_target_position(angle_vert, angle_hori, distance)
        
        if x < 0 and y < 0:
            self.drone.move_left(abs(x))
            self.drone.move_down(abs(y))
        elif x < 0 and y > 0:
            self.drone.move_left(abs(x))
            self.drone.move_up(abs(y))
        elif x > 0 and y > 0:
            self.drone.move_right(abs(x))
            self.drone.move_up(abs(y))
        elif x > 0 and y < 0:
            self.drone.move_right(abs(x))
            self.drone.move_down(abs(y))