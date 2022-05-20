from direction import Direction
import cv2
import utils

t = Direction(cv2.VideoCapture(0))

angle_1, angle_2, length, distance_v = t.check_angles()

print(f"angle_1[degrés]: {round(angle_1, 2)}  angle_2[degrés]: {round(angle_2, 2)}  length: {length}  distance_v[cm]: {round(distance_v, 2)}")

# import json
 
# preset = {"low": "color_list_low", "high": "coesfflor_list_high"}

# with open("presetcolorlist.json", "r+") as json_file:
#     json_load = json.load(json_file)
#     json_load["nafeme"] = preset
#     print(json_load)
#     json_file.seek(0)
#     json.dump(json_load, json_file, indent=4)
#     json_file.close()

# import cv2
# cap = cv2.VideoCapture(0)
# width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
# height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
# print(width, height)