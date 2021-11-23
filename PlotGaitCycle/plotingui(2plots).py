import tkinter as tk, tkinter.ttk as ttk
import matplotlib.pyplot as plt
import matplotlib.backends.backend_tkagg as TkAgg
import numpy as np
import pandas as pd
import win32gui
from PIL import ImageGrab
import time
from datetime import date, datetime


def CaptureScreen():
    HWND = win32gui.GetFocus()
    rect=win32gui.GetWindowRect(HWND)
    print(rect)
    x = rect[0]
    x1=x+root.winfo_width()
    y = rect[1]
    y1=y+root.winfo_height()
    im=ImageGrab.grab((x,y,x1,y1))
    im.save("{}.jpeg".format(str(datetime.now()).replace(':', '.')),'jpeg')

data = pd.read_csv('two_angles.csv')
# data['sideways angle'] = data['sideways angle'] - 90
# data['forward angle'] = data['forward angle'] - 90
table_data = pd.read_csv('stats.csv')
print(table_data.columns)

root = tk.Tk()
root.geometry("{}x{}".format(root.winfo_screenwidth(), root.winfo_screenheight()))

gs_frame = tk.Frame(root, background='#120024',bd=1, relief="flat")
gf1_frame = tk.Frame(root, bd=1, relief="flat")
s_frame = tk.Frame(root, bd=1, relief="flat")

gs_frame.grid(row=0, column=0, sticky="nsew")
gf1_frame.grid(row=0, column=1, sticky="nsew")
s_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

# -----------------------------------------------------------------------------------------------------------------------------------------------

t1 = tk.Label(gs_frame, text="Game Stats", font=("Arial",30), bg='#120024', fg='white').grid(row=0, column=0, columnspan=2, sticky="nsew")

gs21 = tk.Label(gs_frame, height = 3, font=("Arial",13), text="Max Left Lean(deg)", bg='#120024', fg='white').grid(row=1, column=0, sticky="nsew", pady=0)
gs23 = tk.Label(gs_frame, height = 3, font=("Arial",13), text="{}".format(table_data.loc[0, 'Value']), bg='#120024', fg='white').grid(row=1, column=1, sticky="nsew", pady=0)

gs31 = tk.Label(gs_frame, height = 3, font=("Arial",13), text="Max Right Lean(deg)", bg='#120024', fg='white').grid(row=2, column=0, sticky="nsew", pady=0)
gs33 = tk.Label(gs_frame, height = 3, font=("Arial",13), text="{}".format(table_data.loc[1, 'Value']), bg='#120024', fg='white').grid(row=2, column=1, sticky="nsew", pady=0)

gs41 = tk.Label(gs_frame, height = 3, font=("Arial",13), text="Chocolates collected", bg='#120024', fg='white').grid(row=3, column=0, sticky="nsew", pady=0)
gs43 = tk.Label(gs_frame, height = 3, font=("Arial",13), text="-", bg='#120024', fg='white').grid(row=3, column=1, sticky="nsew", pady=0)

gs51 = tk.Label(gs_frame, height = 3, font=("Arial",13), text="No. of times leaned left", bg='#120024', fg='white').grid(row=4, column=0, sticky="nsew", pady=0)
gs53 = tk.Label(gs_frame, height = 3, font=("Arial",13), text="{}".format(int(table_data.loc[2, 'Value'])), bg='#120024', fg='white').grid(row=4, column=1, sticky="nsew", pady=0)

gs61 = tk.Label(gs_frame, height = 3, font=("Arial",13), text="No. of times leaned right", bg='#120024', fg='white').grid(row=5, column=0, sticky="nsew", pady=0)
gs63 = tk.Label(gs_frame, height = 3, font=("Arial",13), text="{}".format(int(table_data.loc[3, 'Value'])), bg='#120024', fg='white').grid(row=5, column=1, sticky="nsew", pady=0)

gs71 = tk.Label(gs_frame, height = 3, font=("Arial",13), text="Time on left(s)", bg='#120024', fg='white').grid(row=6, column=0, sticky="nsew", pady=0)
gs73 = tk.Label(gs_frame, height = 3, font=("Arial",13), text="-", bg='#120024', fg='white').grid(row=6, column=1, sticky="nsew", pady=0)

gs81 = tk.Label(gs_frame, height = 3, font=("Arial",13), text="Time on right(s)", bg='#120024', fg='white').grid(row=7, column=0, sticky="nsew", pady=0)
gs83 = tk.Label(gs_frame, height = 3, font=("Arial",13), text="-", bg='#120024', fg='white').grid(row=7, column=1, sticky="nsew", pady=0)

gs_frame.grid_columnconfigure(0, weight=1)
gs_frame.grid_columnconfigure(1, weight=1)

# -----------------------------------------------------------------------------------------------------------------------------------------------

t2 = tk.Label(gf1_frame, text="Movement Plots", font=("Arial",30), fg='#120024').pack(side='top')

f1, axis1 = plt.subplots(2, 1)

axis1[0].plot(data['Forward angle'])
axis1[0].set_title("Forward flexion angle of hip")
axis1[0].set_ylabel("Angle")

axis1[1].plot(data['Sway_angle'])
axis1[1].set_title("Lateral flexion angle of hip")
axis1[1].set_ylabel("Angle")

plt.tight_layout()

canvas1 = TkAgg.FigureCanvasTkAgg(f1, master=gf1_frame)
canvas1.draw()
## canvas.get_tk_widget().grid(column = 0, row = 0) I'll explain commenting this out below

toolbar1 = TkAgg.NavigationToolbar2Tk(canvas1, gf1_frame)
toolbar1.update()
canvas1._tkcanvas.pack(fill='both', expand=True)
#
# gf1_frame.columnconfigure(0, weight=1)
# gf1_frame.rowconfigure(0, weight=1)
# gf1_frame.rowconfigure(1, weight=12)

# -----------------------------------------------------------------------------------------------------------------------------------------------
root.grid_rowconfigure(0, weight=75)
root.grid_rowconfigure(1, weight=1)

root.grid_columnconfigure(0, weight=2)
root.grid_columnconfigure(1, weight=6)

# -----------------------------------------------------------------------------------------------------------------------------------------------

label = tk.Label(s_frame, text="{}".format(datetime.now()), font=("Arial",20), fg='#120024').grid(sticky="nsew", row=0, column=0)
showScores = tk.Button(s_frame, text="Save as .jpeg", width=20, command=CaptureScreen, bg='#120024', fg='white').grid(row=0,column=1)

s_frame.grid_columnconfigure(0, weight=4)
s_frame.grid_columnconfigure(1, weight=1)

root.mainloop()
