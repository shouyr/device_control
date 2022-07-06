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

waittime = 50
expose = 8000
shotnum = 10
filters = ["F1","F2","F3","F4","F5","F6"]
current_filter = 'F1'
current_count = 500
specmodel = 'MAYP111212'
current_file = 'shot#' + str(shotnum) + current_filter + '_' + specmodel[-3:]

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
def countchange():
    global current_count
    current_count = count.value()
def wait():
    status.setText('ready')
def acquire():
    global current_file
    global shotnum
    current_file = 'shot#' + str(shotnum) + current_filter + '_' + specmodel[-3:]
    filedir.setText(current_file)
    spec = Spectrometer.from_serial_number(serial = specmodel)
    num = np.int32(waittime*1e6/expose)
    spec.integration_time_micros(expose)
    for i in np.arange(num):
        wavelengths, intensities = spec.spectrum(correct_dark_counts = True)
        if np.max(intensities[10:-5]) > current_count:
            break
    dataline.setData(wavelengths, intensities)
    np.save(current_file,intensities)
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

filedir = QTextBrowser()
filedir.setFixedHeight(30)
filedir.setFixedWidth(170)
filedir.setText(current_file)
layout.addWidget(filedir,4,0)

status = QTextBrowser()
status.setFixedHeight(30)
status.setFixedWidth(170)
status.setText('ready')
layout.addWidget(status,4,1)

start = QPushButton('start')
start.clicked.connect(acquire) 
layout.addWidget(start,4,2)


plots = PlotWidget()
plots.setFixedHeight(300)
plots.setFixedWidth(500)
plots.setBackground('w')
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
dataline = plots.plot(data)
plots.showGrid(x=True, y=True)
plots.setXRange(200, 1100, padding=0)
layout.addWidget(plots,5,0,1,3)

timer = QTimer()  # set up your QTimer
timer.timeout.connect(wait)  # connect it to your update function
timer.start(30000)  # set it to timeout in 10000 ms
        
window.setLayout(layout)
window.show()
sys.exit(app.exec_())















