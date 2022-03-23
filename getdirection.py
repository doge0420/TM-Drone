import cv2

def getpixel(mask, x, y, w, h):
    if x or y or w or h == None:
        pass
    
    p1 = mask[int(x+0.25*w), int(y+0.25*h)]
    p2 = mask[int(x+0.75*w), int(y+0.25*h)]
    p3 = mask[int(x+0.25*w), int(y+0.75*h)]
    p4 = mask[int(x+0.75*w), int(y+0.75*h)]
    
    # print(p1, p2, p3, p4)
    
    if p1 and p4 != 0:
        print("\.")
    elif p2 and p3 != 0:
        print("./")