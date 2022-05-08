import cv2
import numpy as np
import utils
from DroneBlocksTelloSimulator.DroneBlocksSimulatorContextManager import DroneBlocksSimulatorContextManager
from djitellopy import Tello
import concurrent.futures

# fonction qui s'active quand les trackbars sont misent à jour (ne fait rien)
def do_nothing(x):
    pass

# création des trackbars
def create_trackbars():
    cv2.namedWindow("trackbar")

    cv2.createTrackbar("low_h_1", "trackbar", 110, 180, do_nothing)    #pour detecter le bleu
    cv2.createTrackbar("low_s_1", "trackbar", 150, 255, do_nothing)
    cv2.createTrackbar("low_v_1", "trackbar", 20, 255, do_nothing)
    cv2.createTrackbar("hi_h_1", "trackbar", 130, 180, do_nothing)
    cv2.createTrackbar("hi_s_1", "trackbar", 255, 255, do_nothing)
    cv2.createTrackbar("hi_v_1", "trackbar", 255, 255, do_nothing)

    cv2.createTrackbar("low_h_2", "trackbar", 170, 180, do_nothing)      #rouge
    cv2.createTrackbar("low_s_2", "trackbar", 151, 255, do_nothing)
    cv2.createTrackbar("low_v_2", "trackbar", 114, 255, do_nothing)
    cv2.createTrackbar("hi_h_2", "trackbar", 180, 180, do_nothing)
    cv2.createTrackbar("hi_s_2", "trackbar", 227, 255, do_nothing)
    cv2.createTrackbar("hi_v_2", "trackbar", 255, 255, do_nothing)

# pour prendre les valeurs des trackbars et faire le masque (rouge)
def blue_mask(image):
    low_h_1 = cv2.getTrackbarPos("low_h_1", "trackbar")
    low_s_1 = cv2.getTrackbarPos("low_s_1", "trackbar")
    low_v_1 = cv2.getTrackbarPos("low_v_1", "trackbar")
    hi_h_1 = cv2.getTrackbarPos("hi_h_1", "trackbar")
    hi_s_1 = cv2.getTrackbarPos("hi_s_1", "trackbar")
    hi_v_1 = cv2.getTrackbarPos("hi_v_1", "trackbar")
    
    lower_1 = np.array([low_h_1, low_s_1, low_v_1])
    upper_1 = np.array([hi_h_1, hi_s_1, hi_v_1])
    
    return cv2.inRange(image, lower_1, upper_1)

# pour prendre les valeurs des trackbars et faire le masque (bleu)
def red_mask(image):
    low_h_2 = cv2.getTrackbarPos("low_h_2", "trackbar")
    low_s_2 = cv2.getTrackbarPos("low_s_2", "trackbar")
    low_v_2 = cv2.getTrackbarPos("low_v_2", "trackbar")
    hi_h_2 = cv2.getTrackbarPos("hi_h_2", "trackbar")
    hi_s_2 = cv2.getTrackbarPos("hi_s_2", "trackbar")
    hi_v_2 = cv2.getTrackbarPos("hi_v_2", "trackbar")
    
    lower_2 = np.array([low_h_2, low_s_2, low_v_2])
    upper_2 = np.array([hi_h_2, hi_s_2, hi_v_2])
    
    return cv2.inRange(image, lower_2, upper_2)

# test avec simulation du drone
def move(angles):
    sim_key = '4fb14a31-7637-4ec9-938e-edc7c980f943'
    distance = 70
    with DroneBlocksSimulatorContextManager(simulator_key=sim_key) as drone:
        if angles[0] < 90 and angles[1] < 90:
            drone.fly_right(distance, "cm")
            drone.fly_up(distance, "cm")
        elif angles[0] < 90 and angles[1] > 90:
            drone.fly_right(distance, "cm")
            drone.fly_down(distance, "cm")
        elif angles[0] > 90 and angles[1] < 90:
            drone.fly_left(distance, "cm")
            drone.fly_up(distance, "cm")
        elif angles[0] > 90 and angles[1] > 90:
            drone.fly_left(distance, "cm")
            drone.fly_down(distance, "cm")

# pas encore fini
def drone():
    drone = Tello()
    drone.connect()

# pour trouver le centre d'un objet et dessiner les contours et le centre
def draw_on_object_center(contours, img):
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

def object_distance(contours, distance):
    if len(contours) != 0:
        for contour in contours:
            if cv2.contourArea(contour) > 350:
                rect = cv2.minAreaRect(contour)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                distance = utils.get_distance(box, distance)
                return distance
    else:
        pass

# fonction pour acquérir les angles et ainsi faire bouger le drone en fonction
def check_angles(video):
    angle_list = []
    distance_list = []
    distance_f_list = []

    create_trackbars()

    for i in range(100):     # capture x image
        _, img = video.read()

        image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # pour avoir les masques
        mask_1 = blue_mask(image)
        mask_2 = red_mask(image)

        # trouver les objets de différentes couleurs
        contours_1, _ = cv2.findContours(mask_1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_2, _ = cv2.findContours(mask_2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # combinaison des deux masques (bleu et rouge)
        mask = mask_1 | mask_2

        # définition des point de départ et d'arrivée de la ligne entre les deux objets
        start = draw_on_object_center(contours_1, img)
        end = draw_on_object_center(contours_2, img)

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
            return utils.unpack((angle_list, object_distance(contours_1, utils.get_median(distance_f_list))))

    cv2.destroyAllWindows()
    return utils.unpack((angle_list, object_distance(contours_1, utils.get_median(distance_f_list))))

if __name__ == '__main__':
    
    video = cv2.VideoCapture(0)
    
    # pour avoir les angles dans un autre thread
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(check_angles, video)
    angle_1, angle_2, length, distance_v = future.result()
    print(f"angle_1[degrés]: {round(utils.get_median(angle_1), 2)}  angle_2[degrés]: {round(utils.get_median(angle_2), 2)}  length: {length}  distance_v[cm]: {round(distance_v, 2)}")