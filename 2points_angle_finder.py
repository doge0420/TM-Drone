import cv2
import numpy as np
import utils

video = cv2.VideoCapture(0)

def empty(x):
    pass

def create_trackbars():
    cv2.namedWindow("trackbar", cv2.WINDOW_FREERATIO)

    cv2.createTrackbar("low_h_1", "trackbar", 110, 180, empty)    #pour detecter le bleu
    cv2.createTrackbar("low_s_1", "trackbar", 150, 255, empty)
    cv2.createTrackbar("low_v_1", "trackbar", 20, 255, empty)
    cv2.createTrackbar("hi_h_1", "trackbar", 130, 180, empty)
    cv2.createTrackbar("hi_s_1", "trackbar", 255, 255, empty)
    cv2.createTrackbar("hi_v_1", "trackbar", 255, 255, empty)

    cv2.createTrackbar("low_h_2", "trackbar", 0, 180, empty)    #rouge
    cv2.createTrackbar("low_s_2", "trackbar", 151, 255, empty)
    cv2.createTrackbar("low_v_2", "trackbar", 114, 255, empty)
    cv2.createTrackbar("hi_h_2", "trackbar", 10, 180, empty)
    cv2.createTrackbar("hi_s_2", "trackbar", 227, 255, empty)
    cv2.createTrackbar("hi_v_2", "trackbar", 255, 255, empty)

# trouver le centre d'un objet et dessiner des trucs dessus
def find_object(contours):
    if len(contours) != 0:
        for contour in contours:
            if cv2.contourArea(contour) > 350:
                rect = cv2.minAreaRect(contour)
                # angle = rect[2]
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                
                x, y = utils.getcenter(box)
                # start, end = utils.getmid(box)
                
                # cv2.line(img, start, end, (0, 255, 0), 3)
                cv2.drawContours(img, [box], 0, (0,0,255), 2)
                cv2.circle(img, (x, y), radius=5, color=(0,255,0), thickness=-1)
                # cv2.putText(img, str(round(angle)), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                return x, y

def get_red(image):
    low_h_1 = cv2.getTrackbarPos("low_h_1", "trackbar")
    low_s_1 = cv2.getTrackbarPos("low_s_1", "trackbar")
    low_v_1 = cv2.getTrackbarPos("low_v_1", "trackbar")
    hi_h_1 = cv2.getTrackbarPos("hi_h_1", "trackbar")
    hi_s_1 = cv2.getTrackbarPos("hi_s_1", "trackbar")
    hi_v_1 = cv2.getTrackbarPos("hi_v_1", "trackbar")
    
    lower_1 = np.array([low_h_1, low_s_1, low_v_1])
    upper_1 = np.array([hi_h_1, hi_s_1, hi_v_1])
    
    return cv2.inRange(image, lower_1, upper_1)

def get_blue(image):
    low_h_2 = cv2.getTrackbarPos("low_h_2", "trackbar")
    low_s_2 = cv2.getTrackbarPos("low_s_2", "trackbar")
    low_v_2 = cv2.getTrackbarPos("low_v_2", "trackbar")
    hi_h_2 = cv2.getTrackbarPos("hi_h_2", "trackbar")
    hi_s_2 = cv2.getTrackbarPos("hi_s_2", "trackbar")
    hi_v_2 = cv2.getTrackbarPos("hi_v_2", "trackbar")
    
    lower_2 = np.array([low_h_2, low_s_2, low_v_2])
    upper_2 = np.array([hi_h_2, hi_s_2, hi_v_2])
    
    return cv2.inRange(image, lower_2, upper_2)

create_trackbars()

while True:
    _, img = video.read()

    image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # pour avoir les masques
    mask_1 = get_red(image)
    mask_2 = get_blue(image)
    
    # trouver les objets de différentes couleurs
    contours_1, _ = cv2.findContours(mask_1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_2, _ = cv2.findContours(mask_2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # combinaison des deux masques
    mask = mask_1 | mask_2
    
    # définition des point de départ et d'arrivée de la ligne entre les deux objets
    start = find_object(contours_1)
    end = find_object(contours_2)

    # print(f"start: {start}")
    # print(f"end: {end}")

    # pour ne pas avoir une ligne si il y a qu'un objet
    if start and end != None:
        cv2.line(img, start, end, (255,0,0), 3)

    cv2.imshow("mask", mask), cv2.imshow("image", img)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break