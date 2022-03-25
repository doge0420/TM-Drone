import cv2

# def getpixel(mask, x, y, w, h):
#     if x or y or w or h == None:
#         pass
    
#     p1 = mask[int(x+0.25*w), int(y+0.25*h)]
#     p2 = mask[int(x+0.75*w), int(y+0.25*h)]
#     p3 = mask[int(x+0.25*w), int(y+0.75*h)]
#     p4 = mask[int(x+0.75*w), int(y+0.75*h)]
    
#     # print(p1, p2, p3, p4)
    
#     if p1 and p4 != 0:
#         print("\.")
#     elif p2 and p3 != 0:
#         print("./")

def getcenter(corners):
    a1, a2 = corners[0]
    b1, b2 = corners[2]
    
    m1 = int((a1+b1)/2)
    m2 = int((a2+b2)/2)
    
    return m1, m2

def getmid(corners):
    a1, a2 = corners[0]
    b1, b2 = corners[1]
    c1, c2 = corners[2]
    d1, d2 = corners[3]
    
    ab1 = int((a1+b1)/2)
    ab2 = int((a2+b2)/2)
    
    cd1 = int((c1+d1)/2)
    cd2 = int((c2+d2)/2)
    
    return (ab1, ab2), (cd1, cd2)