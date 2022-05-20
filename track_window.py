from tkinter import *
from colorutils import Color
import json
import cv2
import numpy as np

class Track_window:
    def __init__(self):
        self.test = True
        self.status = True
        self.current_step = 0

        self.window = Tk()       #création de l'objet fenêtre

        self.window.title("track window")    #titre de la fenêtre
        self.window.geometry("300x100")          #dimensions de bases de la fenetre
        self.window.minsize(300, 100)            #dimensions minimums de la fenêtre
        
        # self.default_color_list, self.default_color_sum, self.default_color_names = self.__import_colors("./color_json/defaultcolorlist.json")
        # self.preset_color_list, self.preset_color_sum, self.preset_color_names = self.__import_colors("./color_json/presetcolorlist.json")
        
        #création du menu (pour quitter)
        self.menubar = Menu(self.window)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Exit", command=self.window.destroy)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.window.config(menu=self.menubar)
        
        # self.color_list_low = [self.default_color_list[0][0], self.default_color_list[0][1], self.default_color_list[0][2]]
        # self.color_list_high = [self.default_color_list[0][3], self.default_color_list[0][4], self.default_color_list[0][5]]

        self.__init_window_content()


    def __init_window_content(self):
        self.step_frame = Frame(self.window)
        self.step_frame.pack()
        self.step_label = Label(self.step_frame, text = "current step: -")
        self.step_label.pack()

        trashbutton = Button(self.window, command=self.next_step, text = "next step")
        trashbutton.pack()

        self.status_frame = Frame(self.window)
        self.status_frame.pack()
        self.status_label = Label(self.status_frame, text = "Waiting for start")
        self.status_label.pack()

    def next_step(self):
        self.current_step += 1
        self.update_current_step(self.current_step)

    def update_current_step(self, cible:int):
        self.step_label['text'] = f"current step: {cible}"

    def update_status(self,text:str):
        self.status_label['text'] = text

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    t = Track_window()
    t.run()