from tkinter import *
import guiutils

window = Tk()

window.title("Color management")
window.geometry("600x600")
window.minsize(600, 600)

#variables declaration
low_h_var = DoubleVar(window)
low_s_var = DoubleVar(window)
low_v_var = DoubleVar(window)
high_h_var = DoubleVar(window)
high_s_var = DoubleVar(window)
high_v_var = DoubleVar(window)

isclosed = False

#color initialisation
low_blue = [110, 150, 20]
high_blue = [130, 255, 255]
blue = low_blue+high_blue

low_green = [10, 10, 10]
high_green = [20, 20, 20]
green = low_green+high_green

low_red = [0, 151, 114]
high_red = [10, 227, 255]
red = low_red+high_red

color_list = [blue, red, green]
color_sum = len(color_list)


low_h_value = None
low_s_value = None
low_v_value = None
high_h_value = None
high_s_value = None
high_v_value = None

#start

guiutils.CreateAdjustmentWindow(window,low_h_var,low_s_var,low_v_var,high_h_var,high_s_var,high_v_var,color_list, color_sum)

window.mainloop()


#update la couleur des previews