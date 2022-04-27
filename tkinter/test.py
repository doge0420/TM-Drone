from tkinter import *
import guiutils
import utils

window = Tk()       #création de l'objet fenêtre

window.title("Color management")    #titre de la fenêtre
window.geometry("600x600")          #dimensions de bases de la fenetre
window.minsize(600, 600)            #dimensions minimums de la fenêtre

#variables declaration
low_h_var = DoubleVar(window)       #créations des variables tkinter de types doublevar (qui correspond a un float)
low_s_var = DoubleVar(window)
low_v_var = DoubleVar(window)
high_h_var = DoubleVar(window)
high_s_var = DoubleVar(window)
high_v_var = DoubleVar(window)

isclosed = False            #boolean qui gère l'état de la fenêtre (ouverte/fermée)

#color initialisation
low_blue = [110, 150, 20]       #stockage des couleurs (min et max) pour faire les filtres ----> passer a un stockage sur un fichier .JSON
high_blue = [130, 255, 255]
blue = low_blue+high_blue

low_green = [10, 10, 10]
high_green = [20, 20, 20]
green = low_green+high_green

low_red = [0, 151, 114]
high_red = [10, 227, 255]
red = low_red+high_red

color_list = [blue, red, green]     #une liste de liste des couleurs
color_sum = len(color_list)

#declaration des variables
low_h_value = None
low_s_value = None
low_v_value = None
high_h_value = None
high_s_value = None
high_v_value = None

#start

# guiutils.CreateAdjustmentWindow(window,low_h_var,low_s_var,low_v_var,high_h_var,high_s_var,high_v_var,color_list, color_sum)        #création de la fenêtre 

utils.init_window(window, color_list)

window.mainloop()           #afficher la fenêtre jusqu'à sa fermeture