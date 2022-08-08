# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 21:18:07 2022

analysis of a laser focal spot with tk GUI
@author: Shou
"""

import tkinter as tk  
import tkinter.filedialog
from PIL import Image,ImageTk
import cv2 
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import rc
import matplotlib.pyplot as plt
x = [0,1]
y = [0,1]
font = {'family' : 'arial',   
  'weight' : 'normal',  
  'size'   : 15,  
  }  
font_size = 15
rc('font', **font)
plt.rcParams['xtick.direction'] = 'in'  # 将x周的刻度线方向设置向内
plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度方向设置向内
plt.rcParams['font.sans-serif']=['arial']
def choosepic():
    num = input1.get()
    if num == '':
        num = '0.109'
    num = np.float64(num)
    path_ = tkinter.filedialog.askopenfilename()
    path.set(path_)
    img_open = Image.open(entry.get())
    image = np.array(img_open)
    # convert to unit8
    tracking = image/np.max(image)*255
    tracking = tracking.astype(np.uint8)
    # grayscale threshold values.
    gmn = np.max(tracking)/10
    gmx = 253
    #apply thresholding to grayscale frames. 
    ret, thresh = cv2.threshold(tracking, gmn, gmx, 0)
    
    # find contours in the threshold image
    contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_TC89_L1)
    
    # finding contour with maximum area and store it as best_cnt
    max_area = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            best_cnt = cnt
    # fitting with a ellipse
    ellipse = cv2.fitEllipse(best_cnt)
    xc = np.int32(ellipse[0][1])
    yc = np.int32(ellipse[0][0])
    a = ellipse[1][0]
    b = ellipse[1][1]
    rmax = 250
    
    # subtract background
    bg = np.mean(tracking[50:150,50:150])
    r = np.arange(rmax)
    sumr = np.zeros(rmax)
    spot0 = tracking[xc-rmax:xc+rmax,yc-rmax:yc+rmax]
    spot0 = spot0 - bg
    sum0 = np.sum(spot0)
    
    for i in r:
        cv2.circle(spot0,(rmax,rmax),i,(0,0,0),-1)
        sumr[i] = np.sum(spot0)
    
    con = (sum0-sumr)/sum0
    cv2.ellipse(tracking,ellipse,(255,0,0),1) #image ellipse(x0 y0 a b theta) color thickness
    spot1 = tracking[xc-rmax:xc+rmax,yc-rmax:yc+rmax]
    spot1 = spot1.astype(np.uint8)
    
    # img = ImageTk.PhotoImage(img_open.resize((500,500)))
    # spot1 = np.resize(spot1,(500,500))
    img = ImageTk.PhotoImage(Image.fromarray(spot1))
    # img = ImageTk.PhotoImage(img.resize((500,500)))
    lableShowImage1.config(image=img)
    lableShowImage1.image = img
    out1.set('a='+str(np.round(a*num,2))+' um  b='+str(np.round(b*num,2)) + ' um,'+' concentration='+str(np.round(con[np.int32(np.max([a,b]))]*100,2))+'%')
    global x ,y
    x = r*num
    y = con
    f.clear()
    ax = f.add_subplot(111)
    ax.plot(x,y)
    ax.set_ylim(0,1)
    ax.set_xlim(0,)
    ax.grid(color='r', linestyle='--', linewidth=1)
    ax.set_xlabel('r (um)',fontdict=font)
    ax.set_ylabel('Concentration',fontdict=font)
    f.subplots_adjust(left=0.12, bottom=0.11, right=0.97, top=0.97,wspace=None, hspace=None)
    canvas.draw_idle()
    
if __name__ == '__main__':
    app = tk.Tk()  
    app.geometry('1024x600') 
    app.title("Laser_spot")  
    can = tk.Canvas(app, bg='white', height=600, width=1024)
    f = Figure(figsize=(5,5), dpi=100)
    a = f.add_subplot(111)
    a.plot(x,y)
    #Entry widget which allows displaying simple text.
    path = tk.StringVar()
    entry = tk.Entry(app, state='readonly', text=path,width = 100)
    entry.grid(columnspan=2)
    lableShowImage1 = tk.Label(app)
    lableShowImage1.grid(row=1,column=0)
    canvas = FigureCanvasTkAgg(f,master=app)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1,column=1)
    buttonSelImage = tk.Button(app, text='open tiff', command=choosepic)
    buttonSelImage.grid(columnspan=2)
    #buttonSelImage.pack(side=tk.BOTTOM)
    #Call the mainloop of Tk.
    input1 = tk.StringVar()
    entry1 = tk.Entry(app,text = input1)
    entry1.grid(row=3,column=0)
    out1 = tk.StringVar()
    entry2 = tk.Entry(app, state='readonly', text=out1,width = 50)
    entry2.grid(row=3,column=1)
    app.mainloop()
    