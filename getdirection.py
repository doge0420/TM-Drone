import cv2

def getpixel(mask, x, y, w, h):
    p1 = mask[int(x+0.25*w), int(y+0.25*h)]
    p2 = mask[int(w*0.75), int(h*0.25)]
    p3 = mask[int(w*0.25), int(h*0.75)]
    p4 = mask[int(w*0.75), int(h*0.75)]
    
    print(p1, p2, p3, p4)