import cv2
from travel import Travel
import utils
import numpy as np
from djitellopy import Tello

class Alignement:
    def __init__(self, drone, travel_obj, test:bool = False):
        self.test = test
        self.drone = drone
        self.travel = travel_obj
        if not self.test:
            self.video = self.drone.get_frame_read()
        if self.test:
            self.video = cv2.VideoCapture(0)
            self.import_mask_color("0")

        self.width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.center = int(self.width/2), int(self.height/2)
        self.__set_roi()

    def import_mask_color(self, cible: str):
        _, _, self.target_color = utils.import_mask_color(cible)

    def __mask(self, image):
        low = self.target_color["low"]
        high = self.target_color["high"]
        
        low_h = low[0]
        low_s = low[1]
        low_v = low[2]

        hi_h = high[0]
        hi_s = high[1]
        hi_v = high[2]

        lower_2 = np.array([low_h, low_s, low_v])
        upper_2 = np.array([hi_h, hi_s, hi_v])

        return cv2.inRange(image, lower_2, upper_2)
    
    # pour trouver le centre d'un objet et dessiner les contours
    def __draw_on_object_and_find_center(self, contours, img):
        if len(contours) != 0:
            for contour in contours:
                if cv2.contourArea(contour) > 400:
                    rect = cv2.minAreaRect(contour)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    x, y = utils.getcenter(box)
                    cv2.drawContours(img, [box], 0, (0,255,0), 2)
                    cv2.circle(img, (x, y), radius=5, color=(0,0,255), thickness=-1)
                    return x, y
        else:
            pass
    
    def __draw_center(self, image):
        cv2.circle(image, self.center, radius=5, color=(0, 0, 255), thickness=-1)
    
    def __draw_line(self, image, object):
        cv2.line(image, self.center, object, color=(0, 0, 255), thickness=2)
        
    def __draw_grid(self, image):
        up_left = (self.a, 0)
        up_right = (self.b,0)
        down_left = (self.a, self.height)
        down_right = (self.b, self.height)
        
        left_up = (0, self.c)
        left_down = (0, self.d)
        right_up = (self.width, self.c)
        right_down = (self.width, self.d)

        cv2.line(image, up_left, down_left, color=(255, 230, 0), thickness=2)
        cv2.line(image, up_right, down_right, color=(255, 230, 0), thickness=2)
        cv2.line(image, left_up, right_up, color=(255, 230, 0), thickness=2)
        cv2.line(image, left_down, right_down, color=(255, 230, 0), thickness=2)
    
    def __set_roi(self):
        self.a = int(self.width * 2/5)
        self.b = int(self.width * 3/5)
        self.c = int(self.height * 2/5)
        self.d = int(self.height * 3/5)

    def __check_roi(self, object: tuple):
        x,y = object
        if x < self.a:
            status = "left"
        elif x > self.b:
            status = "right"
        elif y < self.c:
            status = "up"
        elif y > self.d:
            status = "down"
        else:
            status = "nothing"

        return status

    def align(self):

        stop = 0

        while True:
            if self.test:
                _, img = self.video.read()
            elif not self.test:
                img = self.video.frame
            else:
                print("erreur de test")
            
            image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            self.__set_roi()
            # pour avoir les masques
            mask = self.__mask(image)

            self.__draw_grid(img)

            # trouver les objets de différentes couleurs
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            object = self.__draw_on_object_and_find_center(contours, img)

            if object != None:
                self.__draw_center(img)
                self.__draw_line(img, object)
                status = self.__check_roi(object)
            
                self.travel.lineup(status)
            
                if status == "nothing":
                    stop += 1
                    if stop == 5:
                        if self.test:
                            self.video.release()
                        cv2.destroyAllWindows()
                        break
                else:
                    stop = 0
            
            # affichage de la caméra et du masque
            cv2.imshow("mask", mask), cv2.imshow("image", img) 
        
            if cv2.waitKey(1) & 0xFF == ord("q"):
                if self.test:
                    self.video.release()
                cv2.destroyAllWindows()
                break
                    
if __name__ == '__main__':
    drone = Tello()
    
    a = Alignement(drone)
    a.align()
