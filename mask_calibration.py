import cv2
import numpy as np
import utils
from threading import Thread
from mask_window import color_window

video = cv2.VideoCapture(0)

color_state = 0
color_sum = 2


def win_run():
    global window
    window = color_window()
    window.run()


def main(video):
    global color_state
    global color_sum
    global window

    t = Thread(target=win_run)

    t.start()
    while True:
        _, img = video.read()

        image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = window.get_mask(image)

        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) != 0:
            for contour in contours:
                if cv2.contourArea(contour) > 350:
                    rect = cv2.minAreaRect(contour)
                    angle = rect[2]
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)

                    x, y = utils.getcenter(box)
                    start, end = utils.getmid(box)

                    cv2.line(img, start, end, (0, 255, 0), 3)
                    cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
                    cv2.circle(img, (x, y), radius=5,
                               color=(0, 255, 0), thickness=-1)
                    cv2.putText(img, str(round(angle)), (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        cv2.imshow("mask", mask), cv2.imshow("image", img)

        if cv2.waitKey(1) & 0xFF == ord("q") or window.get_status() == False:
            cv2.destroyAllWindows()
            t.join()
            break

if __name__ == '__main__':
    main(video)