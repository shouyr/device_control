# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 14:33:42 2022
auto-acquiring and save using Oceanoptics maya200pro
@author: shouy
"""

from PyQt5.QtWidgets import (QLabel, QApplication, QPushButton, QWidget, QGridLayout, QComboBox,  QInputDialog, QSpinBox, QTextBrowser)
from pyqtgraph import PlotWidget
import numpy as np
import sys
from PyQt5.QtCore import QTimer
from seabreeze.spectrometers import Spectrometer
# import time
waittime = 20
expose = 10000
shotnum = 10
filters = ["F1","F2","F3","F4","F5","F6"]
flipper1 = ["b0","b1"]
flipper2 = ["d0","d1"]
current_filter = 'F1'
current_flp1 = 'b0'
current_flp2 = 'd0'
notes = ''
current_count = 2000
specmodel = 'MAYP111332'
current_file = 'shot#' + str(shotnum) + current_filter + '_' + specmodel[-3:] + '_' + current_flp1 + '_' + current_flp2 + '_' + notes

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('Ocean Optics')
layout = QGridLayout()


def name1():
    text, ok = QInputDialog.getText(window, 'name', 'input the name')
    global specmodel
    if ok:
        btn1.setText(text)
        specmodel = text        
def valuechange1():
    global waittime
    waittime = time1.value()
def valuechange2():
    global expose
    expose = time2.value()
def shotchange():
    global shotnum
    shotnum = shotn.value()
def filterchange():
    global current_filter
    current_filter = cb.currentText()
def flipper1change():
    global current_flp1
    current_flp1 = flp1.currentText()
def flipper2change():
    global current_flp2
    current_flp2 = flp2.currentText()
def changenote():
    text, ok = QInputDialog.getText(window, 'name', 'input the name')
    global notes
    if ok:
        btn32.setText(text)
        notes = text
def countchange():
    global current_count
    current_count = count.value()
def wait():
    status.setText('ready')
def acquire():
    global current_file
    global shotnum
    #current_file = 'shot#' + str(shotnum) + current_filter + '_' + specmodel[-3:] + '_' + current_flp1 + '_' + current_flp2 + '_' + notes
    current_file = 'shot#' + str(shotnum) + current_filter + '_' + specmodel[-3:] + '_' + notes
    filedir.setText(current_file)
    spec = Spectrometer.from_serial_number(serial = specmodel)
    num = np.int32(waittime*1e6/expose)
    print(num)
    # t1 = time.time()
    spec.integration_time_micros(expose)
    for i in np.arange(num):
        wavelengths, intensities = spec.spectrum(correct_dark_counts = True)
        if np.max(intensities[10:-5]) > current_count:
            break
        else: 
            # time.sleep(0.01)
            numt = np.int32(waittime-i*expose/1e6)
            if numt < num: 
                status.setText(str(numt+1))
                status.repaint() #立即重绘
                QApplication.processEvents()
                num = numt
    dataline.setData(wavelengths, intensities)
    np.savetxt(current_file+'_x.txt',wavelengths,fmt='%10.5f')
    np.savetxt(current_file+'.txt',intensities,fmt='%10.5f')
    # t2 = time.time()
    # print(t2-t1)
    shotnum = shotnum + 1
    shotn.setValue(shotnum)
    status.setText('OK')
    spec.close()
    
lab1 = QLabel("Serial#")
layout.addWidget(lab1,0,0)
lab2 = QLabel("Totaltime(s)")
layout.addWidget(lab2,0,1)
lab3 = QLabel("time(us)")
layout.addWidget(lab3,0,2)

btn1 = QPushButton('MAYP111212')
btn1.clicked.connect(name1) 
layout.addWidget(btn1,1,0)

time1 = QSpinBox()
time1.setRange(1,1000)
time1.setValue(20)
time1.valueChanged.connect(valuechange1) 
layout.addWidget(time1,1,1)

time2 = QSpinBox() 
time2.setRange(7200,65000000)
time2.setValue(8000)
time2.valueChanged.connect(valuechange2) 
layout.addWidget(time2,1,2)

lab4 = QLabel("Shot#")
layout.addWidget(lab4,2,0)
lab5 = QLabel("Filter")
layout.addWidget(lab5,2,1)
lab6 = QLabel("Threshold")
layout.addWidget(lab6,2,2)

shotn = QSpinBox()
shotn.setRange(1,1000)
shotn.setValue(50)
shotn.valueChanged.connect(shotchange) 
layout.addWidget(shotn,3,0)

cb = QComboBox()
cb.addItems(filters)
cb.currentIndexChanged.connect(filterchange)
layout.addWidget(cb,3,1)

count = QSpinBox() 
count.setRange(100,65535)
count.setValue(500)
count.valueChanged.connect(countchange) 
layout.addWidget(count,3,2)

lab7 = QLabel("Flipper_800nm")
layout.addWidget(lab7,4,0)
lab8 = QLabel("Flipper_400nm")
layout.addWidget(lab8,4,1)
lab9 = QLabel("Notes")
layout.addWidget(lab9,4,2)

flp1 = QComboBox()
flp1.addItems(flipper1)
flp1.currentIndexChanged.connect(flipper1change)
layout.addWidget(flp1,5,0)

flp2 = QComboBox()
flp2.addItems(flipper2)
flp2.currentIndexChanged.connect(flipper2change)
layout.addWidget(flp2,5,1)

btn32 = QPushButton('')
btn32.clicked.connect(changenote) 
layout.addWidget(btn32)

filedir = QTextBrowser()
filedir.setFixedHeight(30)
filedir.setFixedWidth(170)
filedir.setText(current_file)
layout.addWidget(filedir,6,0)

status = QTextBrowser()
status.setFixedHeight(30)
status.setFixedWidth(170)
status.setText('ready')
layout.addWidget(status,6,1)

start = QPushButton('start')
start.clicked.connect(acquire) 
layout.addWidget(start,6,2)


plots = PlotWidget()
plots.setFixedHeight(300)
plots.setFixedWidth(500)
plots.setBackground('w')
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
dataline = plots.plot(data)
plots.showGrid(x=True, y=True)
plots.setXRange(200, 1100, padding=0)
layout.addWidget(plots,7,0,1,3)

timer = QTimer()  # set up your QTimer
timer.timeout.connect(wait)  # connect it to your update function
timer.start(30000)  # set it to timeout in 10000 ms
        
window.setLayout(layout)
window.show()
sys.exit(app.exec_())















