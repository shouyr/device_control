# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 21:18:07 2022

analysis of a laser focal spot with tk GUI
@author: Shou
"""


import tkinter as tk  
import tkinter.filedialog
from PIL import Image,ImageTk,ImageGrab
import win32gui
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
    global path_
    path_ = tkinter.filedialog.askopenfilename()
    path.set(path_)
    refresh()
    
def CaptureScreen():
    HWND = win32gui.GetFocus()
    rect=win32gui.GetWindowRect(HWND)
    x0 = rect[0]
    x1=x0+1001
    y0 = rect[1]
    y1=y0+640
    im=ImageGrab.grab((x0,y0,x1,y1))
    im.save(path_[0:-4]+'.jpg','jpeg')
    np.savetxt(path_[0:-4]+'.txt',xyout.T,header='first column x in unit um and second column concentration',fmt='%.4f')
    with open("result.txt", "ab") as f:
        np.savetxt(f, resout,fmt='%.3e', header=path_.encode("utf-8").decode("latin1")+': 1/e^2 a/2,'+' b/2,'+' sqrt(ab)/2,'+' concentration; '+' FWHM a,'+' b,'+' sqrt(ab),'+' concentration; '+' intensity;',newline='  ', footer='\n',comments='')
        
# you can use other keys and replace it with "<Return>". EX: "f"
# by default, this function will pass an unknown argument to your function.
# thus, you have to give your function a parameter; in this case, we will use *args
def refresh(*args):
    num = input1.get()
    num = np.float64(num)
    spot_size = input2.get()
    spot_size = np.float64(spot_size)
    laser_energy = input3.get()
    laser_energy = np.float64(laser_energy)
    laser_t = input4.get()
    laser_t = np.float64(laser_t)
    background = input5.get()
    background = np.float64(background)
    img_open = Image.open(path_)
    image = np.array(img_open)
    image = cv2.medianBlur(image,3)
    maxpixel = inputa.get()
    maxpixel = np.float64(maxpixel)
    minpixel = inputb.get()
    minpixel = np.float64(minpixel)
    # convert to unit8
    tracking = image/np.max(image)*255
    tracking = tracking.astype(np.uint8)
    # grayscale threshold values.
    gmn = np.max(tracking)/10
    gmx = 253
    #apply thresholding to grayscale frames. 
    ret, thresh = cv2.threshold(tracking, gmn, gmx, 0)
    global resout
    resout = np.zeros(9)
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
    rmax = np.int32(spot_size/num)
    
    tracking2 = image/np.max(image[xc-rmax:xc+rmax,yc-rmax:yc+rmax])*255
    tracking2 = tracking2.astype(np.uint8)
    # grayscale threshold values.
    gmn = np.max(tracking2)/2.71828/2.71828
    gmx = 255
    #apply thresholding to grayscale frames. 
    ret, thresh = cv2.threshold(tracking2, gmn, gmx, 0)
    
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
    
    sumr = np.zeros(rmax)
    spot0 = image[xc-rmax:xc+rmax,yc-rmax:yc+rmax]
    # subtract background
    bg = np.mean(image[50:150,50:150])
    out4.set('auto_background='+str(np.round(bg,4)))
    if background != 0: 
        bg = background
    r = np.arange(rmax)
    spot0 = spot0 - bg
    sum0 = np.sum(spot0)
    
    for i in r:
        cv2.circle(spot0,(rmax,rmax),i,(0,0,0),-1)
        sumr[i] = np.sum(spot0)
    
    con = (sum0-sumr)/(sum0-sumr[-1])
    cv2.ellipse(tracking2,ellipse,(255,0,0),1) #image ellipse(x0 y0 a b theta) color thickness
    spot1 = tracking2[xc-rmax:xc+rmax,yc-rmax:yc+rmax]
    spot1 = spot1.astype(np.uint8)
    
    spot0 = image-bg
    cv2.ellipse(spot0,ellipse,(0,0,0),-1)
    sum1 = np.sum(spot0[xc-rmax:xc+rmax,yc-rmax:yc+rmax])
    cone2 = (sum0-sum1)/(sum0-sumr[-1]) 
    spot1[spot1>maxpixel] = maxpixel
    spot1[spot1<minpixel] = minpixel
    spot1 = (spot1-minpixel)/(np.max(spot1)-minpixel)*255
    img = Image.fromarray(np.uint8(spot1), mode="L")
    img = img.resize((500,500))
    img = ImageTk.PhotoImage(img)
    lableShowImage1.config(image=img)
    lableShowImage1.image = img
    out1.set('1/e^2 a/2='+str(np.round(a*num/2,2))+' b/2='+str(np.round(b*num/2,2)) + ' '+'√ab/2='+str(np.round(np.sqrt(a*b)*num/2,2)) + ' um,'+' concentration='+str(np.round(cone2*100,2))+'%')
    resout[0:4]=[a*num/2,b*num/2, np.sqrt(a*b)*num/2,cone2]

    tracking3 = image/np.max(image[xc-rmax:xc+rmax,yc-rmax:yc+rmax])*255
    tracking3 = tracking3.astype(np.uint8)
    # grayscale threshold values.
    gmn = np.max(tracking3)/2.0
    gmx = 255
    #apply thresholding to grayscale frames. 
    ret, thresh = cv2.threshold(tracking3, gmn, gmx, 0)
    
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
    spot0 = image-bg
    cv2.ellipse(spot0,ellipse,(0,0,0),-1)
    sum1 = np.sum(spot0[xc-rmax:xc+rmax,yc-rmax:yc+rmax])
    confwhm = (sum0-sum1)/(sum0-sumr[-1]) 
    out2.set('FWHM a='+str(np.round(a*num,2))+' b='+str(np.round(b*num,2)) + ' '+'√ab='+str(np.round(np.sqrt(a*b)*num,2)) + ' um,'+' concentration='+str(np.round(confwhm*100,2))+'%')
    intensity = 4*np.log(2)*laser_energy/np.pi/laser_t*1e15/a/b/num/num*1e8*confwhm/0.5
    out3.set('intensity = ' + str(format(intensity, '.2e')) + ' W/cm^2')
    resout[4:9]=[a*num,b*num,np.sqrt(a*b)*num,confwhm,intensity]
    
    global x ,y, xyout
    x = r*num
    y = con
    xyout = np.zeros((2,np.size(y)))
    xyout[0,:] = x
    xyout[1,:] = y
    f.clear()
    ax = f.add_subplot(111)
    ax.plot(x,y)
    ax.set_ylim(0,1.05)
    ax.set_xlim(0,)
    ax.grid(color='r', linestyle='--', linewidth=1)
    ax.set_xlabel('r (um)',fontdict=font)
    ax.set_ylabel('Concentration',fontdict=font)
    ax.axvline((a+b)*0.25*num,linewidth='2',linestyle=':',alpha=1.0)
    f.subplots_adjust(left=0.12, bottom=0.11, right=0.97, top=0.97,wspace=None, hspace=None)
    canvas.draw_idle()
    
if __name__ == '__main__':
    app = tk.Tk()  
    app.geometry('1001x640') 
    app.title("Laser_spot")  
    can = tk.Canvas(app, bg='white', height=640, width=1001)
    f = Figure(figsize=(5,5), dpi=100)
    a = f.add_subplot(111)
    a.plot(x,y)
    #Entry widget which allows displaying simple text.
    path = tk.StringVar()
    entry = tk.Entry(app, state='readonly', text=path,width = 100)
    entry.grid(columnspan=6)
    lableShowImage1 = tk.Label(app)
    lableShowImage1.grid(row=1,column=0,columnspan=3)
    canvas = FigureCanvasTkAgg(f,master=app)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1,column=3,columnspan=3)
    buttonSelImage = tk.Button(app, text='open tiff image', command=choosepic)
    buttonSelImage.grid(row=2,column=0)
    buttonCapture = tk.Button(app, text='save the result', command=CaptureScreen)
    buttonCapture.grid(row=2,column=5)
    #buttonSelImage.pack(side=tk.BOTTOM)
    #Call the mainloop of Tk.
    label1 = tk.Label(app, text="calibration um/pixel")
    label1.grid(row=3,column=0)
    input1 = tk.StringVar(value = '0.1324')
    entry1 = tk.Entry(app,text = input1)
    entry1.bind('<Return>',refresh)
    entry1.grid(row=3,column=1)
    out1 = tk.StringVar()
    entry2 = tk.Entry(app, state='readonly', text=out1,width = 60)
    entry2.grid(row=5,column=0,columnspan=4)
    labela = tk.Label(app, text="                   Max pixel value (0-255)",anchor='e')
    labela.grid(row=2,column=3)
    inputa = tk.StringVar(value = '255')
    entrya = tk.Entry(app,text = inputa)
    entrya.bind('<Return>',refresh)
    entrya.grid(row=2,column=4)
    labelb = tk.Label(app, text="                   Min pixel value (0-255)",anchor='e')
    labelb.grid(row=2,column=1)
    inputb = tk.StringVar(value = '0')
    entryb = tk.Entry(app,text = inputb)
    entryb.bind('<Return>',refresh)   
    entryb.grid(row=2,column=2)
    input2 = tk.StringVar(value = '60')
    entry3 = tk.Entry(app,text = input2)
    entry3.bind('<Return>',refresh)
    entry3.grid(row=3,column=3)
    label2 = tk.Label(app, text="plot_size_um")
    label2.grid(row=3,column=2)
    out2 = tk.StringVar()
    entry4 = tk.Entry(app, state='readonly', text=out2,width = 60)
    entry4.grid(row=6,column=0,columnspan=4)
    input3 = tk.StringVar(value = '30')
    entry5 = tk.Entry(app,text = input3)
    entry5.bind('<Return>',refresh)
    entry5.grid(row=4,column=4)
    label3 = tk.Label(app, text="laser_energy_J")
    label3.grid(row=3,column=4)
    input4 = tk.StringVar(value = '25')
    entry6 = tk.Entry(app,text = input4)
    entry6.bind('<Return>',refresh)
    entry6.grid(row=4,column=5)
    label4 = tk.Label(app, text="laser_duration_fs")
    label4.grid(row=3,column=5)
    out3 = tk.StringVar()
    entry7 = tk.Entry(app, state='readonly', text=out3,width = 30,font=("Arial 12"))
    entry7.grid(row=5,column=4,columnspan=2,rowspan=2)
    input5 = tk.StringVar(value = '0')
    entry8 = tk.Entry(app,text = input5)
    entry8.bind('<Return>',refresh)
    entry8.grid(row=4,column=3)
    label4 = tk.Label(app, text="set_background")
    label4.grid(row=4,column=2)
    out4 = tk.StringVar()
    entry9 = tk.Entry(app, state='readonly', text=out4,width = 30)
    entry9.grid(row=4,column=0,columnspan=2)
    app.mainloop()
    