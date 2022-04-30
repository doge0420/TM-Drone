from tkinter import *
from colorutils import Color

#les fonction prints_value sont les callbacks des trackbars qui servent a update les previews et garder les values à jour
def Print_low_h(val):
    global low_h_value
    global low_s_value
    global low_v_value
    global high_h_value
    global high_s_value
    global high_v_value
    global low_canvas
    global high_canvas
    global low_preview
    global high_preview
    low_h_value = int(val)
    UpdatePreviewColor(low_canvas,high_canvas,low_preview,high_preview,low_h_value, low_s_value, low_v_value, high_h_value, high_s_value, high_v_value)

def Print_low_s(val):
    global low_h_value
    global low_s_value
    global low_v_value
    global high_h_value
    global high_s_value
    global high_v_value
    global low_canvas
    global high_canvas
    global low_preview
    global high_preview
    low_s_value = int(val)
    UpdatePreviewColor(low_canvas,high_canvas,low_preview,high_preview,low_h_value, low_s_value, low_v_value, high_h_value, high_s_value, high_v_value)

def Print_low_v(val):
    global low_h_value
    global low_s_value
    global low_v_value
    global high_h_value
    global high_s_value
    global high_v_value
    global low_canvas
    global high_canvas
    global low_preview
    global high_preview
    low_v_value = int(val)
    UpdatePreviewColor(low_canvas,high_canvas,low_preview,high_preview,low_h_value, low_s_value, low_v_value, high_h_value, high_s_value, high_v_value)

def Print_high_h(val):
    global low_h_value
    global low_s_value
    global low_v_value
    global high_h_value
    global high_s_value
    global high_v_value
    global low_canvas
    global high_canvas
    global low_preview
    global high_preview
    high_h_value = int(val)
    UpdatePreviewColor(low_canvas,high_canvas,low_preview,high_preview,low_h_value, low_s_value, low_v_value, high_h_value, high_s_value, high_v_value)

def Print_high_s(val):
    global low_h_value
    global low_s_value
    global low_v_value
    global high_h_value
    global high_s_value
    global high_v_value
    global low_canvas
    global high_canvas
    global low_preview
    global high_preview
    high_s_value = int(val)
    UpdatePreviewColor(low_canvas,high_canvas,low_preview,high_preview,low_h_value, low_s_value, low_v_value, high_h_value, high_s_value, high_v_value)

def Print_high_v(val):
    global low_h_value
    global low_s_value
    global low_v_value
    global high_h_value
    global high_s_value
    global high_v_value
    global low_canvas
    global high_canvas
    global low_preview
    global high_preview
    high_v_value = int(val)
    UpdatePreviewColor(low_canvas,high_canvas,low_preview,high_preview,low_h_value, low_s_value, low_v_value, high_h_value, high_s_value, high_v_value)

#cette fonction crée la fenetre avec tous les composants intégrés
def CreateAdjustmentWindow(window,low_h_var,low_s_var,low_v_var,high_h_var,high_s_var,high_v_var,color_list, color_sum):
    global low_h_trackbar
    global low_s_trackbar
    global low_v_trackbar
    global high_h_trackbar
    global high_s_trackbar
    global high_v_trackbar
    global low_preview
    global high_preview
    global low_canvas
    global high_canvas
    global isclosed
    global color_state
    global low_h_value
    global low_s_value
    global low_v_value
    global high_h_value
    global high_s_value
    global high_v_value
#initialisations et déclaration des variables
    color_state = 0
    low_h_value = None
    low_s_value = None
    low_v_value = None
    high_h_value = None
    high_s_value = None
    high_v_value = None
#création du menu (pour quitter)
    menubar = Menu(window)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Exit", command=lambda:Close(window))
    menubar.add_cascade(label="File", menu=filemenu)
    window.config(menu=menubar)
    
#création des deux frames qui organisent la disposition des trackbars et des previews
    low_frame = Frame(window)
    low_frame.pack()
    low_scale_frame = Frame(low_frame, bg = "#1170F6")
    low_scale_frame.pack(fill = BOTH, expand = True, side = LEFT)
    low_canvas = Canvas(low_frame, height = 70, width = 70)
    low_canvas.pack(side = RIGHT)
    low_preview = low_canvas.create_rectangle(0, 0, 70, 70)

    high_frame = Frame(window)
    high_frame.pack()
    high_scale_frame = Frame(high_frame, bg = "#D40B8A")
    high_scale_frame.pack(fill = BOTH, expand = True, side = LEFT)
    high_canvas = Canvas(high_frame, height = 70, width = 70)
    high_canvas.pack(side = RIGHT)
    high_preview = high_canvas.create_rectangle(0, 0, 70, 70) 

#création des trackbars 

    low_h_trackbar = Scale(
        low_scale_frame,        #destination
        variable = low_h_var,   #variable associée (pas sur qu'elle soit utile)
        orient = HORIZONTAL,    #oriantation
        to = 180,               #valeur max
        command = Print_low_h,  #callback
        length = 200            #longueur graphique de la trackbar
    )
    low_h_trackbar.pack(anchor=CENTER)      #ajout graphique de la trackbar dans "window"

    low_s_trackbar = Scale(
        low_scale_frame,
        variable = low_s_var,
        orient = HORIZONTAL,
        to = 255,
        command = Print_low_s,
        length = 200
    )
    low_s_trackbar.pack(anchor=CENTER)

    low_v_trackbar = Scale(
        low_scale_frame,
        variable = low_v_var,
        orient = HORIZONTAL,
        to = 255,
        command = Print_low_v,
        length = 200
    )
    low_v_trackbar.pack(anchor=CENTER)

    high_h_trackbar = Scale(
        high_scale_frame,
        variable = high_h_var,
        orient = HORIZONTAL,
        to = 180,
        command = Print_high_h,
        length = 200
    )
    high_h_trackbar.pack(anchor=CENTER)

    high_s_trackbar = Scale(
        high_scale_frame,
        variable = high_s_var,
        orient = HORIZONTAL,
        to = 255,
        command = Print_high_s,
        length = 200
    )
    high_s_trackbar.pack(anchor=CENTER)

    high_v_trackbar = Scale(
        high_scale_frame,
        variable = high_v_var,
        orient = HORIZONTAL,
        to = 255,
        command = Print_high_v,
        length = 200
    )
    high_v_trackbar.pack(anchor=CENTER)
#création des deux boutons (switch et print)
    switch_button = Button(
        window,                     #destination
        text = "switch color",      #texte visible
        command = lambda:UpdateColor(color_list, color_sum)     #fonction du bouton
    )
    switch_button.pack(             #ajout graphique du bouton dans "window"
        side = BOTTOM,              #emplacement de destination
        expand = True               #prends le plus de place possible (pas collé au sol par exemple)
    )

    print_button = Button(
        window,
        text="print values",
        command = PrintValues
    )
    print_button.pack(
        side = BOTTOM,
        expand = True
    )
    UpdateColor(color_list, color_sum)          #on appelle une première fois cette fonction pour initialiser la position des trackbars
    
#cette fonction est appelée au démarrage et lors de l'utilisation du bouton switch
def UpdateColor(color_list, color_sum):
    global color_state 

    color_state = color_state % color_sum       #reste de la division par le nombre de couleurs (si 3 couleurs en tout et state =4, alors state devient 1)
    current_color = color_list[color_state]     #sélection de la bonne couleur de la color list que l'on stocke sous "current_color" en fonction du color_state
    color_state += 1                            #passage au prochain "state"
    SetValues(current_color) #on set les valeurs de la nouvelles couleur sur les trackbars
    
#fonction utilisée uniquement par l'intermédiaire du bouton switch 
def SetValues(current_color):
    global low_h_trackbar
    global low_s_trackbar
    global low_v_trackbar
    global high_h_trackbar
    global high_s_trackbar
    global high_v_trackbar

    low_h_trackbar.set(current_color[0])        #on set toutes les trackbars avec les valeurs de la nouvelle couleur actuelle
    low_s_trackbar.set(current_color[1])
    low_v_trackbar.set(current_color[2])
    high_h_trackbar.set(current_color[3])
    high_s_trackbar.set(current_color[4])
    high_v_trackbar.set(current_color[5])
    
#fonction utilisée par le menu "exit"
def Close(window):
    global isclosed
    window.destroy()
    isclosed = True     #pas encore utile mais pourra l'être afin d'effectuer des actions à la fin
    
#fonction utile pour debug uniquement
def PrintValues():
    global current_values
    global low_h_value
    global low_s_value
    global low_v_value
    global high_h_value
    global high_s_value
    global high_v_value
    current_values = [low_h_value, low_s_value, low_v_value, high_h_value, high_s_value, high_v_value]
    print(current_values)
    
#fonction qui retourne une liste contenant les valeurs des trackbars au moment de l'appel de cette derniière
def GetValues():
    global current_values
    return current_values

#fonction qui prends en paramètres les 3 valeurs du code couleur HSV pour retourner le code hexadécimal (utile pour update les previews des couleurs)
def HSVtoHEX(h_value, s_value, v_value):
    HSV = Color(hsv=(float(h_value)*2-1, float(s_value)/255, float(v_value)/255))
    HEX = HSV.hex
    return HEX

#est appelée dans les callbacks du début du script et set les couleur des previews avec les codes HEX déduits des codes HSV
def UpdatePreviewColor(low_canvas,high_canvas,low_preview,high_preview,low_h_value, low_s_value, low_v_value, high_h_value, high_s_value, high_v_value):
    low_canvas.itemconfig(low_preview, outline=HSVtoHEX(low_h_value, low_s_value, low_v_value), fill=HSVtoHEX(low_h_value, low_s_value, low_v_value))
    high_canvas.itemconfig(high_preview, outline=HSVtoHEX(high_h_value, high_s_value, high_v_value), fill=HSVtoHEX(high_h_value, high_s_value, high_v_value))
    
# ///////////////////////////////////////////////////////////////////////