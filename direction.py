import cv2
import numpy as np
import utils

class Direction:
    def __init__(self, video):
        self.video = video  
        self.import_mask("0")

    # ouvre color_order.json pour obtenir les ranges de couleurs dans l'ordre du parcours
    def import_mask(self, cible: str):
        self.first_colors, self.second_colors, _ = utils.import_mask(cible)

    # crée le masque pour le premier objet
    def first_mask(self, image):
        first_low = self.first_colors["low"]
        first_high = self.first_colors["high"]

        low_h = first_low[0]
        low_s = first_low[1]
        low_v = first_low[2]

        hi_h = first_high[0]
        hi_s = first_high[1]
        hi_v = first_high[2]

        lower_1 = np.array([low_h, low_s, low_v])
        upper_1 = np.array([hi_h, hi_s, hi_v])
        
        return cv2.inRange(image, lower_1, upper_1)

    # crée le masque pour le deuxième objet
    def second_mask(self, image):
        second_low = self.second_colors["low"]
        second_high = self.second_colors["high"]

        low_h = second_low[0]
        low_s = second_low[1]
        low_v = second_low[2]

        hi_h = second_high[0]
        hi_s = second_high[1]
        hi_v = second_high[2]

        lower_2 = np.array([low_h, low_s, low_v])
        upper_2 = np.array([hi_h, hi_s, hi_v])
        
        return cv2.inRange(image, lower_2, upper_2)
    
    # pour dessiner les contours et trouver le centre de l'objet
    def draw_on_object_and_find_center(self, contours, img):
        if len(contours) != 0:
            for contour in contours:
                if cv2.contourArea(contour) > 350:
                    rect = cv2.minAreaRect(contour)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    x, y = utils.getcenter(box)
                    cv2.drawContours(img, [box], 0, (0,0,255), 2)
                    cv2.circle(img, (x, y), radius=5, color=(0,255,0), thickness=-1)
                    return x, y
        else:
            pass
        
    # pour obtenir la vraie distance entre deux objets avec les cotés verticaux de notre objet de refenrence (le premier masque)
    def object_distance(self, contours, distance):
        if len(contours) != 0:
            for contour in contours:
                if cv2.contourArea(contour) > 400:
                    rect = cv2.minAreaRect(contour)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    distance = utils.get_distance(box, distance)
                    return distance
        else:
            pass
        
    # fonction pour acquérir les angles et ainsi faire bouger le drone en fonction
    def check_angles(self):
        angle_list = []
        distance_list = []
        distance_f_list = []

        for i in range(100):     # capture x image
            _, img = self.video.read()

            image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            # pour avoir les masques
            mask_1 = self.first_mask(image)
            mask_2 = self.second_mask(image)

            # trouver les objets de différentes couleurs
            contours_1, _ = cv2.findContours(mask_1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours_2, _ = cv2.findContours(mask_2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # combinaison des deux masques (bleu et rouge)
            mask = mask_1 | mask_2

            # définition des point de départ et d'arrivée de la ligne entre les deux objets
            start = self.draw_on_object_and_find_center(contours_1, img)
            end = self.draw_on_object_and_find_center(contours_2, img)

            # pour ne pas avoir de ligne s'il n'y a qu'un objet détécté
            if start and end != None:
                horizontal = (1000, start[1])
                vertical = (start[0], -1000)
                cv2.line(img, start, end, (255,0,0), 3)   # pour dessiner la ligne entre les objets
                cv2.line(img, start, horizontal, (0,255,0), 2)  # pour dessiner l'axe horizontal
                cv2.line(img, start, vertical, (0,255,0), 2)    # pour dessiner l'axe vertical
                angles = utils.get_angles(start, end)       # retourne les angles entre les deux axes sous forme de tuple
                distance_f = utils.get_two_points_distance(start, end)
                distance_list.append(distance_f)
                cv2.putText(img, f"angle horizontal: {str(angles[0])}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)    #text avec angle
                cv2.putText(img, f"angle vertical: {str(angles[1])}", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)      #text avec angle
                angle_list.append(angles)   # ajoute les angles à la liste

            if distance_list:
                distance_f = utils.get_median(distance_list)
                distance_f_list.append(distance_f)
                
            cv2.imshow("mask", mask), cv2.imshow("image", img)  # affichage de la caméra et des deux masques combinés

            if cv2.waitKey(1) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                return utils.unpack((angle_list, self.object_distance(contours_1, utils.get_median(distance_f_list))))

        cv2.destroyAllWindows()
        return utils.unpack((angle_list, self.object_distance(contours_1, utils.get_median(distance_f_list))))