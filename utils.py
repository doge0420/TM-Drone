from math import sqrt, acos, degrees

from numpy import float16, float32

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

def get_angles(start, end):
    
    d1x = end[0]-start[0]
    d1y = end[1]-start[1]
    d2x = 1000-start[0]
    d2y = 0
    
    d1x_2 = 0
    d1y_2 = -1000-start[1]
    d2x_2 = end[0]-start[0]
    d2y_2 = end[1]-start[1]
    
    return float16(degrees(acos((d1x*d2x)/(sqrt(d1x ** 2+d1y ** 2)*sqrt(d2x ** 2+d2y ** 2))))), float16(degrees(acos((d1y_2*d2y_2)/(sqrt(d1x_2 ** 2+d1y_2 ** 2)*sqrt(d2x_2 ** 2+d2y_2 ** 2)))))