
from tkinter import *
from colorutils import Color

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

    color_state = 0
    low_h_value = None
    low_s_value = None
    low_v_value = None
    high_h_value = None
    high_s_value = None
    high_v_value = None

    menubar = Menu(window)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Exit", command=lambda:Close(window))
    menubar.add_cascade(label="File", menu=filemenu)
    window.config(menu=menubar)

    low_frame = Frame(window)
    low_frame.pack()
    low_scale_frame = Frame(low_frame, bg = "#1170F6")
    low_scale_frame.pack(fill = BOTH, expand = True, side = LEFT)
    low_canvas = Canvas(low_frame, height = 70, width = 70)
    low_canvas.pack(side = RIGHT)
    low_preview = low_canvas.create_rectangle(0, 0, 70, 70, outline = "blue", fill = "blue")

    high_frame = Frame(window)
    high_frame.pack()
    high_scale_frame = Frame(high_frame, bg = "#D40B8A")
    high_scale_frame.pack(fill = BOTH, expand = True, side = LEFT)
    high_canvas = Canvas(high_frame, height = 70, width = 70)
    high_canvas.pack(side = RIGHT)
    high_preview = high_canvas.create_rectangle(0, 0, 70, 70, outline = "red", fill = "red")



    low_h_trackbar = Scale(
        low_scale_frame,
        variable = low_h_var,
        orient = HORIZONTAL,
        to = 180,
        command = Print_low_h,
        length = 200
    )
    low_h_trackbar.pack(anchor=CENTER)

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

    switch_button = Button(
        window,
        text = "switch color",
        command = lambda:UpdateColor(color_list, color_sum)
    )
    switch_button.pack(
        side = BOTTOM,
        expand = True
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
    UpdateColor(color_list, color_sum)

def UpdateColor(color_list, color_sum):
    global color_state

    color_state = color_state % color_sum
    current_color = color_list[color_state]
    color_state += 1
    SetValues(current_color)

def SetValues(current_color):
    global low_h_trackbar
    global low_s_trackbar
    global low_v_trackbar
    global high_h_trackbar
    global high_s_trackbar
    global high_v_trackbar

    low_h_trackbar.set(current_color[0])
    low_s_trackbar.set(current_color[1])
    low_v_trackbar.set(current_color[2])
    high_h_trackbar.set(current_color[3])
    high_s_trackbar.set(current_color[4])
    high_v_trackbar.set(current_color[5])

def Close(window):
    global isclosed
    window.destroy()
    isclosed = True

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

def GetValues():
    global current_values
    return current_values

def HSVtoHEX(h_value, s_value, v_value):
    HSV = Color(hsv=(float(h_value)*2, float(s_value)/255, float(v_value)/255))
    HEX = HSV.hex
    return HEX

def UpdatePreviewColor(low_canvas,high_canvas,low_preview,high_preview,low_h_value, low_s_value, low_v_value, high_h_value, high_s_value, high_v_value):
    low_canvas.itemconfig(low_preview, outline=HSVtoHEX(low_h_value, low_s_value, low_v_value), fill=HSVtoHEX(low_h_value, low_s_value, low_v_value))
    high_canvas.itemconfig(high_preview, outline=HSVtoHEX(high_h_value, high_s_value, high_v_value), fill=HSVtoHEX(high_h_value, high_s_value, high_v_value))