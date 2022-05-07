from tkinter import *
from colorutils import Color
import json
import cv2
import numpy as np

def import_colors(file_name: str):
    with open(file_name, 'r') as json_file:
        json_load = json.load(json_file)
    json_file.close()

    color_list = []
    color_names = []
    color_ids = []
    for key in json_load.keys():
        color_names.append(key)
        id = json_load[key]["id"]       #pas utile pour l'instant mais peut l'être dans le futur
        color_ids.append(id)
        key = json_load[key]["low"]+json_load[key]["high"]
        color_list.append(key)

    return color_list,len(color_list),color_names,color_ids

def init_window():
    global color_list_low
    global color_list_high
    global color_list
    global color_state
    global color_sum
    global color_names
    global color_ids
    global test
    global status

    test = True
    status = True

    window = Tk()       #création de l'objet fenêtre

    window.title("Color management")    #titre de la fenêtre
    window.geometry("600x600")          #dimensions de bases de la fenetre
    window.minsize(600, 600)            #dimensions minimums de la fenêtre

    tello = None
    
    color_list,color_sum,color_names,color_ids = import_colors("colorlist.json")
    color_state = 0
    
    #création du menu (pour quitter)
    menubar = Menu(window)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Exit", command=lambda:close(window,tello))
    menubar.add_cascade(label="File", menu=filemenu)
    window.config(menu=menubar)
    
    color_list_low = [color_list[0][0], color_list[0][1], color_list[0][2]]
    color_list_high = [color_list[0][3], color_list[0][4], color_list[0][5]]

    init_trackbars(window)
    window.mainloop()           #afficher la fenêtre jusqu'à sa fermeture

def intit_low_preview(window):
    global low_preview
    global low_canvas
    
    #création des deux frames qui organisent la disposition des trackbars et des previews
    low_frame = Frame(window)
    low_frame.pack()
    low_scale_frame = Frame(low_frame, bg = "#1170F6")
    low_scale_frame.pack(fill = BOTH, expand = True, side = LEFT)
    low_canvas = Canvas(low_frame, height = 70, width = 70)
    low_canvas.pack(side = RIGHT)
    low_preview = low_canvas.create_rectangle(0, 0, 70, 70)

    return low_scale_frame

def init_high_preview(window):
    global high_preview
    global high_canvas
    
    #création des deux frames qui organisent la disposition des trackbars et des previews
    high_frame = Frame(window)
    high_frame.pack()
    high_scale_frame = Frame(high_frame, bg = "#D40B8A")
    high_scale_frame.pack(fill = BOTH, expand = True, side = LEFT)
    high_canvas = Canvas(high_frame, height = 70, width = 70)
    high_canvas.pack(side = RIGHT)
    high_preview = high_canvas.create_rectangle(0, 0, 70, 70)
    
    return high_scale_frame
    
def init_trackbars(window):
    global high_h_trackbar
    global high_s_trackbar
    global high_v_trackbar
    global low_h_trackbar
    global low_s_trackbar
    global low_v_trackbar

    low_scale_frame = intit_low_preview(window)
    high_scale_frame = init_high_preview(window)

    
    #création des trackbars 
    high_h_trackbar = Scale(
        high_scale_frame,
        
        orient = HORIZONTAL,
        to = 180,
        command = callback_high_1,
        length = 200
    )
    high_h_trackbar.pack(anchor=CENTER)

    high_s_trackbar = Scale(
        high_scale_frame,
        
        orient = HORIZONTAL,
        to = 255,
        command = callback_high_2,
        length = 200
    )
    high_s_trackbar.pack(anchor=CENTER)

    high_v_trackbar = Scale(
        high_scale_frame,

        orient = HORIZONTAL,
        to = 255,
        command = callback_high_3,
        length = 200
    )
    high_v_trackbar.pack(anchor=CENTER)
    
    low_h_trackbar = Scale(
        low_scale_frame,        #destination
                                #variable associée (pas sur qu'elle soit utile)
        orient = HORIZONTAL,    #oriantation
        to = 180,               #valeur max
        command = callback_low_1,  #callback
        length = 200            #longueur graphique de la trackbar
    )
    low_h_trackbar.pack(anchor=CENTER)      #ajout graphique de la trackbar dans "window"

    low_s_trackbar = Scale(
        low_scale_frame,
        
        orient = HORIZONTAL,
        to = 255,
        command = callback_low_2,
        length = 200
    )
    low_s_trackbar.pack(anchor=CENTER)

    low_v_trackbar = Scale(
        low_scale_frame,
        
        orient = HORIZONTAL,
        to = 255,
        command = callback_low_3,
        length = 200
    )
    low_v_trackbar.pack(anchor=CENTER)
    
    #création des deux boutons (switch et print)
    print_button = Button(
        window,
        text="print values",
        command = print_values
    )
    print_button.pack(
        side = BOTTOM,
        expand = True
    )
    #le bouton switch a été remplacé pas les boutons de couleur
    # switch_button = Button(
    #     window,                     #destination
    #     text = "switch color",      #texte visible
    #     command = switch_color      #fonction du bouton
    # )
    # switch_button.pack(             #ajout graphique du bouton dans "window"
    #     side = BOTTOM,              #emplacement de destination
    #     expand = True               #prends le plus de place possible (pas collé au sol par exemple)
    # )

    color_buttons_frame = Frame(window)
    color_buttons_frame.pack(
        side = BOTTOM,
        expand = True
    )
#création des boutons de couleur
    column_var = 0 
    row_var = 0
    for index in range(color_sum):
        create_color_button(index,color_buttons_frame,row_var,column_var)
        row_var += 1
        column_var += 0.5
    
    low_h_trackbar.set(color_list_low[0])
    low_s_trackbar.set(color_list_low[1])      
    low_v_trackbar.set(color_list_low[2])
    high_h_trackbar.set(color_list_high[0])
    high_s_trackbar.set(color_list_high[1])
    high_v_trackbar.set(color_list_high[2])
    
def close(window,tello):
    global test
    global status
    window.destroy()
    if not test:
        tello.end()
    status = False

def callback_low_1(value):
    value_list_low(value, 0)
    
def callback_low_2(value):
    value_list_low(value, 1)
    
def callback_low_3(value):
    value_list_low(value, 2)
        
def value_list_low(value, index):
    global color_list_low
    
    color_list_low[index] = int(value)
    
    update_low_preview()

def update_low_preview():
    global color_list_low
    global low_canvas
    
    color = HSVtoHEX(color_list_low[0], color_list_low[1], color_list_low[2])
    low_canvas.itemconfig(low_preview, outline=color, fill=color)
    
def callback_high_1(value):
    value_list_high(value, 0)
    
def callback_high_2(value):
    value_list_high(value, 1)
    
def callback_high_3(value):
    value_list_high(value, 2)
        
def value_list_high(value, index):
    global color_list_high
    
    color_list_high[index] = int(value)
    
    update_high_preview()
    
def update_high_preview():
    global color_list_high
    global high_canvas
    
    color = HSVtoHEX(color_list_high[0], color_list_high[1], color_list_high[2])
    high_canvas.itemconfig(high_preview, outline=color, fill=color)
    
def HSVtoHEX(h_value, s_value, v_value):
    HSV = Color(hsv=(float(h_value)*2-1, float(s_value)/255, float(v_value)/255))
    HEX = HSV.hex
    return HEX

def print_values():
    global color_list_low
    global color_list_high
    
    print(f"high_list: {color_list_high}\nlow_list: {color_list_low}")
    
# def switch_color():
#     global color_list
#     global color_state
#     global color_sum

#     color_state = color_state % color_sum
#     current_color = color_list[color_state]
#     color_state += 1
#     set_values(current_color)

def set_values(current_color):
    low_h_trackbar.set(current_color[0])
    low_s_trackbar.set(current_color[1])      
    low_v_trackbar.set(current_color[2])
    high_h_trackbar.set(current_color[3])
    high_s_trackbar.set(current_color[4])
    high_v_trackbar.set(current_color[5])


def get_values():
    global color_list_low
    global color_list_high
    return color_list_low,color_list_high

def create_color_button(index,color_buttons_frame,row_var,column_var):   
    color_button = Button(
        color_buttons_frame,
        text = import_colors("colorlist.json")[2][index],
        height = 2,
        width = 10,
        bg = HSVtoHEX(import_colors("colorlist.json")[0][index][3],import_colors("colorlist.json")[0][index][4],import_colors("colorlist.json")[0][index][5]),
        command = lambda index=index:set_values(import_colors("colorlist.json")[0][index])
        # command = print(import_colors("colorlist.json")[0][i])
    )
    row = row_var % 2
    column = int(column_var)
    color_button.grid(
        column = column,
        row = row,
        padx = 10,
        pady = 10
        )

def get_mask(image):
    low, up = get_values()
    
    lower = np.array([low])
    upper = np.array([up])
    
    return cv2.inRange(image, lower, upper)

def get_status():
    global status
    return status