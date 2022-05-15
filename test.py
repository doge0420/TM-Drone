# from two_points_angle_and_range_finder import direction
# import cv2
# import utils

# t = direction(cv2.VideoCapture(0))

# angle_1, angle_2, length, distance_v = t.check_angles()

# print(f"angle_1[degrés]: {round(utils.get_median(angle_1), 2)}  angle_2[degrés]: {round(utils.get_median(angle_2), 2)}  length: {length}  distance_v[cm]: {round(distance_v, 2)}")

import json

preset = {"low": "color_list_low", "high": "coesfflor_list_high"}

with open("presetcolorlist.json", "r+") as json_file:
    json_load = json.load(json_file)
    json_load["nafeme"] = preset
    print(json_load)
    json_file.seek(0)
    json.dump(json_load, json_file, indent=4)
    json_file.close()
