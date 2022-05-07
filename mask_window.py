from tkinter import *
from colorutils import Color
import json
import cv2
import numpy as np

class color_window():
    def __init__(self):
        self.test = True
        self.status = True

        self.window = Tk()       #création de l'objet fenêtre

        self.window.title("Color management")    #titre de la fenêtre
        self.window.geometry("600x600")          #dimensions de bases de la fenetre
        self.window.minsize(600, 600)            #dimensions minimums de la fenêtre

        self.tello = None
        
        self.color_list, self.color_sum, self.color_names, self.color_ids = self.__import_colors("colorlist.json")
        self.color_state = 0
        
        #création du menu (pour quitter)
        self.menubar = Menu(self.window)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Exit", command=self.close)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.window.config(menu=self.menubar)
        
        self.color_list_low = [self.color_list[0][0], self.color_list[0][1], self.color_list[0][2]]
        self.color_list_high = [self.color_list[0][3], self.color_list[0][4], self.color_list[0][5]]

        self.__init_trackbars()

    def __init_low_preview(self):
        
        #création des deux frames qui organisent la disposition des trackbars et des previews
        low_frame = Frame(self.window)
        low_frame.pack()
        low_scale_frame = Frame(low_frame, bg = "#1170F6")
        low_scale_frame.pack(fill = BOTH, expand = True, side = LEFT)
        self.low_canvas = Canvas(low_frame, height = 70, width = 70)
        self.low_canvas.pack(side = RIGHT)
        self.low_preview = self.low_canvas.create_rectangle(0, 0, 70, 70)

        return low_scale_frame
    
    def __init_high_preview(self):
        
        #création des deux frames qui organisent la disposition des trackbars et des previews
        high_frame = Frame(self.window)
        high_frame.pack()
        high_scale_frame = Frame(high_frame, bg = "#D40B8A")
        high_scale_frame.pack(fill = BOTH, expand = True, side = LEFT)
        self.high_canvas = Canvas(high_frame, height = 70, width = 70)
        self.high_canvas.pack(side = RIGHT)
        self.high_preview = self.high_canvas.create_rectangle(0, 0, 70, 70)
        
        return high_scale_frame
    
    def __init_trackbars(self):

        low_scale_frame = self.__init_low_preview()
        high_scale_frame = self.__init_high_preview()

        #création des trackbars 
        self.high_h_trackbar = Scale(
            high_scale_frame,
            
            orient = HORIZONTAL,
            to = 180,
            command = self.__callback_high_1,
            length = 200
        )
        self.high_h_trackbar.pack(anchor=CENTER)

        self.high_s_trackbar = Scale(
            high_scale_frame,
            
            orient = HORIZONTAL,
            to = 255,
            command = self.__callback_high_2,
            length = 200
        )
        self.high_s_trackbar.pack(anchor=CENTER)

        self.high_v_trackbar = Scale(
            high_scale_frame,

            orient = HORIZONTAL,
            to = 255,
            command = self.__callback_high_3,
            length = 200
        )
        self.high_v_trackbar.pack(anchor=CENTER)
        
        self.low_h_trackbar = Scale(
            low_scale_frame,        #destination
                                    #variable associée (pas sur qu'elle soit utile)
            orient = HORIZONTAL,    #oriantation
            to = 180,               #valeur max
            command = self.__callback_low_1,  #callback
            length = 200            #longueur graphique de la trackbar
        )
        self.low_h_trackbar.pack(anchor=CENTER)      #ajout graphique de la trackbar dans "window"

        self.low_s_trackbar = Scale(
            low_scale_frame,
            
            orient = HORIZONTAL,
            to = 255,
            command = self.__callback_low_2,
            length = 200
        )
        self.low_s_trackbar.pack(anchor=CENTER)

        self.low_v_trackbar = Scale(
            low_scale_frame,
            
            orient = HORIZONTAL,
            to = 255,
            command = self.__callback_low_3,
            length = 200
        )
        self.low_v_trackbar.pack(anchor=CENTER)
        
        #création des deux boutons (switch et print)
        self.print_button = Button(
            self.window,
            text="print values",
            command = self.__print_values
        )
        self.print_button.pack(
            side = BOTTOM,
            expand = True
        )

        color_buttons_frame = Frame(self.window)
        color_buttons_frame.pack(
            side = BOTTOM,
            expand = True
        )
    #création des boutons de couleur
        column_var = 0 
        row_var = 0
        for index in range(self.color_sum):
            self.__create_color_button(index,color_buttons_frame,row_var,column_var)
            row_var += 1
            column_var += 0.5
        
        self.low_h_trackbar.set(self.color_list_low[0])
        self.low_s_trackbar.set(self.color_list_low[1])      
        self.low_v_trackbar.set(self.color_list_low[2])
        self.high_h_trackbar.set(self.color_list_high[0])
        self.high_s_trackbar.set(self.color_list_high[1])
        self.high_v_trackbar.set(self.color_list_high[2])
        
    def close(self):
        self.window.destroy()
        self.status = False
        
    def __callback_low_1(self, value):
        self.__value_list_low(value, 0)
    
    def __callback_low_2(self, value):
        self.__value_list_low(value, 1)
        
    def __callback_low_3(self, value):
        self.__value_list_low(value, 2)
            
    def __value_list_low(self, value, index):
        
        self.color_list_low[index] = int(value)
        self.__update_low_preview()

    def __update_low_preview(self):

        color = self.__HSVtoHEX(self.color_list_low[0], self.color_list_low[1], self.color_list_low[2])
        self.low_canvas.itemconfig(self.low_preview, outline=color, fill=color)
        
    def __callback_high_1(self, value):
        self.__value_list_high(value, 0)
    
    def __callback_high_2(self, value):
        self.__value_list_high(value, 1)
        
    def __callback_high_3(self, value):
        self.__value_list_high(value, 2)
            
    def __value_list_high(self, value, index):
        
        self.color_list_high[index] = int(value)
        self.__update_high_preview()
        
    def __update_high_preview(self):

        color = self.__HSVtoHEX(self.color_list_high[0], self.color_list_high[1], self.color_list_high[2])
        self.high_canvas.itemconfig(self.high_preview, outline=color, fill=color)
        
    def __HSVtoHEX(self, h_value, s_value, v_value):
        HSV = Color(hsv=(float(h_value)*2-1, float(s_value)/255, float(v_value)/255))
        HEX = HSV.hex
        return HEX

    def __print_values(self):
        print(f"high_list: {self.color_list_high}\nlow_list: {self.color_list_low}")
        
    def __set_values(self, current_color):
        self.low_h_trackbar.set(current_color[0])
        self.low_s_trackbar.set(current_color[1])      
        self.low_v_trackbar.set(current_color[2])
        self.high_h_trackbar.set(current_color[3])
        self.high_s_trackbar.set(current_color[4])
        self.high_v_trackbar.set(current_color[5])

    def __get_values(self):
        return self.color_list_low, self.color_list_high
    
    def __create_color_button(self, index, color_buttons_frame, row_var, column_var): 
          
        color_list, length, color_names, color_ids = self.__import_colors("colorlist.json")
        
        color_button = Button(
            color_buttons_frame,
            text = color_names[index],
            height = 2,
            width = 10,
            bg = self.__HSVtoHEX(color_list[index][3], color_list[index][4], color_list[index][5]),
            command = lambda index=index:self.__set_values(color_list[index])
        )
        row = row_var % 2
        column = int(column_var)
        color_button.grid(
            column = column,
            row = row,
            padx = 10,
            pady = 10
            )
        
    def __import_colors(self, file_name: str):
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

        return color_list, len(color_list), color_names, color_ids
    
    def get_mask(self, image):
        low, up = self.__get_values()
        
        lower = np.array([low])
        upper = np.array([up])
        
        return cv2.inRange(image, lower, upper)

    def get_status(self):
        return self.status
    
    def run(self):
        self.window.mainloop()           #afficher la fenêtre jusqu'à sa fermeture 