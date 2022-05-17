from math import sqrt, acos, degrees
from numpy import float16
import statistics
import json

# pour avoir les coordonée du centre de la boite (n'est plus utile)
def getcenter(corners):
    a1, a2 = corners[0]
    b1, b2 = corners[2]
    
    m1 = int((a1+b1)/2)
    m2 = int((a2+b2)/2)
    
    return m1, m2

# pour avoir les coordonée du centre des coté de la boite (n'est plus utile)
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

# pour avoir les angles entres les axes et l'objet bleu, respectivement horizontal et vertical
def get_angles(start, end):
    
    d1x = end[0]-start[0]
    d1y = end[1]-start[1]
    d2x = 1000-start[0]
    d2y = 0
    
    d1x_2 = 0
    d1y_2 = -1000-start[1]
    d2x_2 = end[0]-start[0]
    d2y_2 = end[1]-start[1]
    
    return float16(degrees(acos((d1x*d2x)/(sqrt(d1x**2+d1y**2)*sqrt(d2x**2+d2y**2))))), float16(degrees(acos((d1y_2*d2y_2)/(sqrt(d1x_2**2+d1y_2**2)*sqrt(d2x_2**2+d2y_2**2)))))

# pour avoir deux listes d'angles correspondant à leur axes et aussi la taille des listes
def unpack(tuple: tuple):
    angles_horiz = []
    angles_verti = []
    list_of_tuples = tuple[0]
    distance = tuple[1]
    length = len(list_of_tuples)
    
    for tuple in list_of_tuples:
        angle_1, angle_2 = tuple
        angles_horiz.append(angle_1)
        angles_verti.append(angle_2)

    return angles_horiz, angles_verti, length, distance

# pour avoir la distance entre deux points
def get_two_points_distance(start, end):
    d1 = end[0]-start[0]
    d2 = end[1]-start[1]

    distance = sqrt(d1**2+d2**2)

    return distance

# pour avoir la vraie distance entre les deux objets de couleur [cm] avec les cotés verticaux de l'objet de ref
def get_distance(box, distance_f):
    a1, a2 = box[0]
    b1, b2 = box[1]
    c1, c2 = box[2]
    d1, d2 = box[3]
    
    g1, g2 = c1-a1, c2-a2
    d1, d2 = d1-b1, d2-b2
    
    g = sqrt(g1**2+g2**2)
    d = sqrt(d1**2+d2**2)
    
    vert_side_measured_average = float16((g+d)/2)
    vert_side_real_size = 5 #cm
    
    return (distance_f*vert_side_real_size)/vert_side_measured_average

# pour avoir la mediane d'une liste
def get_median(list):
    return statistics.median(list)

def import_mask(cible):
    with open("./color_json/color_order.json", "r") as file:
            json_file = json.load(file)
            file.close()
            json_file = json_file[cible]
            first_colors = json_file["first"]
            second_colors = json_file["second"]
            target_colors = json_file["target"]
            
            return first_colors, second_colors, target_colors