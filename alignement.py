import cv2
from travel import Travel
import utils
import numpy as np

class Alignement:
    def __init__(self, video):
        self.video = video 
        self.width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.center = int(self.width/2), int(self.height/2)
        self.import_mask("0")

    def import_mask(self, cible: str):
        _, _, self.target_color = utils.import_mask(cible)

    def mask(self, image):
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
    def draw_on_object_and_find_center(self, contours, img):
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
    
    def draw_center(self, image):
        cv2.circle(image, self.center, radius=5, color=(0, 0, 255), thickness=-1)
    
    def draw_line(self, image, object):
        cv2.line(image, self.center, object, color=(0, 0, 255), thickness=2)
        
    def draw_grid(self, image):
        up_left = (int(self.width/3), 0)
        up_right = (int(2*self.width/3), 0)
        down_left = (int(self.width/3), self.height)
        down_right = (int(2*self.width/3), self.height)
        
        left_up = (0, int(self.height/3))
        left_down = (0, int(2*self.height/3))
        right_up = (self.width, int(self.height/3))
        right_down = (self.width, int(2*self.height/3))
    
        cv2.line(image, up_left, down_left, color=(255, 230, 0), thickness=2)
        cv2.line(image, up_right, down_right, color=(255, 230, 0), thickness=2)
        cv2.line(image, left_up, right_up, color=(255, 230, 0), thickness=2)
        cv2.line(image, left_down, right_down, color=(255, 230, 0), thickness=2)
    
    def align(self):

        while True:
            _, img = self.video.read()
            image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            # pour avoir les masques
            mask = self.mask(image)

            self.draw_grid(img)

            # trouver les objets de différentes couleurs
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            object = self.draw_on_object_and_find_center(contours, img)
        
            if object != None:
                self.draw_center(img)
                self.draw_line(img, object)
        
            # affichage de la caméra et du masque
            cv2.imshow("mask", mask), cv2.imshow("image", img) 
        
            if cv2.waitKey(1) & 0xFF == ord("q"):
                    cv2.destroyAllWindows()
                    break
                    
if __name__ == '__main__':
    video = cv2.VideoCapture(0)
    
    a = Alignement(video)
    a.align()