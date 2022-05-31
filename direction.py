import cv2
import numpy as np
from travel import Travel
import utils
from time import sleep

class Direction:
    def __init__(self, drone, travel_obj, test: bool = False):
        self.test = test
        self.drone = drone
        self.travel = travel_obj

    # ouvre color_order.json pour obtenir les ranges de couleurs dans l'ordre du parcours
    def import_mask_color(self, cible: str):
        self.first_colors, self.second_colors, _ = utils.import_mask_color(cible)

    # crée le masque pour le premier objet
    def __first_mask(self, image):
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
    def __second_mask(self, image):
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
    def __draw_on_object_and_find_center(self, contours, img):
        if len(contours) != 0:
            for contour in contours:
                if cv2.contourArea(contour) > 350:
                    rect = cv2.minAreaRect(contour)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    x, y = utils.getcenter(box)
                    cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
                    cv2.circle(img, (x, y), radius=5,
                               color=(0, 255, 0), thickness=-1)
                    return x, y
        else:
            pass

    # pour obtenir la vraie distance entre deux objets avec les cotés verticaux de notre objet de refenrence (le premier masque)
    def __object_distance(self, contours, distance):
        if len(contours) != 0:
            for contour in contours:
                if cv2.contourArea(contour) > 400:
                    rect = cv2.minAreaRect(contour)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    distance = utils.get_distance(box, distance)
                    return distance
        else:
            print("ok")

    # fonction pour acquérir les angles et ainsi faire bouger le drone en fonction
    def check_angles(self, cible):
        angle_list = []
        distance_list = []
        frame = 0

        if not self.test:
            self.video = self.drone.get_frame_read()
        if self.test:
            self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            self.import_mask_color(cible)

        while True:     # capture x image
            if not self.test:
                img = self.video.frame
                img = cv2.resize(img, (640, 480))
            else:
                _, img = self.video.read()

            image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            # pour avoir les masques
            mask_1 = self.__first_mask(image)
            mask_2 = self.__second_mask(image)

            # trouver les objets de différentes couleurs
            contours_1, _ = cv2.findContours(
                mask_1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours_2, _ = cv2.findContours(
                mask_2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # combinaison des deux masques (bleu et rouge)
            mask = mask_1 | mask_2

            # définition des point de départ et d'arrivée de la ligne entre les deux objets
            start = self.__draw_on_object_and_find_center(contours_1, img)
            end = self.__draw_on_object_and_find_center(contours_2, img)

            # pour ne pas avoir de ligne s'il n'y a qu'un objet détécté
            if start and end != None:
                horizontal = (1000, start[1])
                vertical = (start[0], -1000)
                # pour dessiner la ligne entre les objets
                cv2.line(img, start, end, (255, 0, 0), 3)
                # pour dessiner l'axe horizontal
                cv2.line(img, start, horizontal, (0, 255, 0), 2)
                # pour dessiner l'axe vertical
                cv2.line(img, start, vertical, (0, 255, 0), 2)
                # retourne les angles entre les deux axes sous forme de tuple
                angles = utils.get_angles(start, end)
                distance_pixel = utils.get_two_points_distance(start, end)
                distance_list.append(distance_pixel)
                cv2.putText(img, f"angle horizontal: {str(angles[0])}", (
                    50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)  # text avec angle
                cv2.putText(img, f"angle vertical: {str(angles[1])}", (
                    50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)  # text avec angle
                angle_list.append(angles)   # ajoute les angles à la liste

                # check si on a plus que x mesures et fini le loop si la condition est remplie
                if len(distance_list) >= 30:
                    if self.test:
                        self.video.release()
                    cv2.destroyAllWindows()
                    return utils.unpack((angle_list, self.__object_distance(contours_1, utils.get_median(distance_list))))

            # affichage de la caméra et des deux masques combinés
            cv2.imshow("mask", mask), cv2.imshow("image", img)

            frame += 1

            # check chaque x frame si on a plus que y mesure dans distance_list
            if frame == 200:
                if len(distance_list) < 30:
                    frame = 0
                    print("pas assez de mesures", len(distance_list))
                    essai = self.travel.search()
                    sleep(2)
                if essai > 3:
                    if self.test:
                        self.video.release()
                    cv2.destroyAllWindows()
                    break
            # pour quitter la fenetre au cas ou
            if cv2.waitKey(1) & 0xFF == ord("q"):
                if self.test:
                    self.video.release()
                cv2.destroyAllWindows()
                break
