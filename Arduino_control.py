from PyQt5.QtWidgets import (QApplication, QPushButton, QWidget, QSlider, QGridLayout, QComboBox, QLabel, QMessageBox)
from PyQt5.QtCore import Qt, QTimer
from QLed import QLed
import serial
import serial.tools.list_ports
import sys
  #readline after write to clean the buffer          
def oepn_serial():
    global ser
    comstr = cb.currentText()
    ser = serial.Serial(comstr[0:4], 9600, timeout=1)
    if ser.isOpen() == True:
        led.value = True

def close_serial():
    ser.close()
    led.value = ser.isOpen()
def selectionchange():
    led.value = False
          
def open1():
    ser.write(b'1')
    led1.value = True
    
def close1():
    ser.write(b'0')
    led1.value = False
    
def open2():
    ser.write(b'3')
    led2.value = True
    
def close2():
    ser.write(b'2')
    led2.value = False


def quit1():
    sys.exit()
    
port_list = list(serial.tools.list_ports.comports())
tempstr = ["none","none","none","none","none","none","none","none","none","none"]
if len(port_list) == 0:
   tempstr[0] = 'serial not found'
else:
    for i in range(0,len(port_list)):
        tempstr[i] = str(port_list[i])      
        
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('ESM Shutter')
layout = QGridLayout()

cb = QComboBox()
cb.addItems(tempstr)
cb.currentIndexChanged.connect(selectionchange)
layout.addWidget(cb,0,0)

led = QLed(onColour=QLed.Blue, shape=QLed.Circle)
led.value = False
layout.addWidget(led,0,1)
        
btn1 = QPushButton('oepn_serial')
btn1.clicked.connect(oepn_serial)
layout.addWidget(btn1,1,0)

btn2 = QPushButton('close_serial')
btn2.clicked.connect(close_serial) 
layout.addWidget(btn2,1,1)

led1 = QLed(onColour=QLed.Yellow, shape=QLed.Round)
led1.value = False
layout.addWidget(led1,2,0)

btn10 = QPushButton('ESM1 on')
btn10.clicked.connect(open1) 
layout.addWidget(btn10,2,1)

btn11 = QPushButton('ESM1 off')
btn11.clicked.connect(close1) 
layout.addWidget(btn11,2,2)

led2 = QLed(onColour=QLed.Yellow, shape=QLed.Round)
led2.value = False
layout.addWidget(led2,3,0)

btn20 = QPushButton('ESM2 on')
btn20.clicked.connect(open2) 
layout.addWidget(btn20,3,1)

btn21 = QPushButton('ESM2 off')
btn21.clicked.connect(close2) 
layout.addWidget(btn21,3,2)


window.setLayout(layout)
window.show()
sys.exit(app.exec_())
