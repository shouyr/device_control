from PyQt5.QtWidgets import *
from QLed import QLed
import serial
import serial.tools.list_ports
import sys
def selectionchange():
    ser.close()
def oepn_serial():
    global ser
    comstr = cb.currentText()
    ser = serial.Serial(comstr[0:4], 9600, timeout=1)
    if ser.isOpen() == True:
        led.value = True
        ser.write(b'\x01\x0F\x00\x00\x00\x10\x02\x00\x00\xE2\x20') #close all
        led1.value = False
        led2.value = False
        led3.value = False
        led4.value = False
    else:
        alert = QMessageBox()
        alert.setText('serial problem')
        alert.exec()
        led.value = False
   # return ser
def close_serial():
    ser.close()
    led.value = ser.isOpen()
    
def updataled():
    ser.write(b'\x01\x03\x00\x00\x00\x10\x3D\xC6')
def open1():
    ser.write(b'\x01\x05\x00\x00\xFF\x00\x8C\x3A')
    led1.value = True
def close1():
    ser.write(b'\x01\x05\x00\x00\x00\x00\xCD\xCA')
    led1.value = False
def name1():
    text, ok = QInputDialog.getText(window, 'name', 'input the name')
    if ok:
        btn12.setText(text)
def open2():
    ser.write(b'\x01\x05\x00\x01\xFF\x00\xDD\xFA')
    led2.value = True
def close2():
    ser.write(b'\x01\x05\x00\x01\x00\x00\x9C\x0A')
    led2.value = False
def name2():
    text, ok = QInputDialog.getText(window, 'name', 'input the name')
    if ok:
        btn22.setText(text)        
def open3():
    ser.write(b'\x01\x05\x00\x02\xFF\x00\x2D\xFA')
    led3.value = True
def close3():
    ser.write(b'\x01\x05\x00\x02\x00\x00\x6C\x0A')
    led3.value = False
def name3():
    text, ok = QInputDialog.getText(window, 'name', 'input the name')
    if ok:
        btn32.setText(text)
def open4():
    ser.write(b'\x01\x05\x00\x03\xFF\x00\x7C\x3A')
    led4.value = True
def close4():
    ser.write(b'\x01\x05\x00\x03\x00\x00\x3D\xCA')
    led4.value = False
def name4():
    text, ok = QInputDialog.getText(window, 'name', 'input the name')
    if ok:
        btn42.setText(text)
        
port_list = list(serial.tools.list_ports.comports())
tempstr = ["none","none","none","none","none","none","none","none","none","none"]
if len(port_list) == 0:
   tempstr[0] = 'serial not found'
else:
    for i in range(0,len(port_list)):
        tempstr[i] = str(port_list[i])      
        
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('Remote Realy')
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
layout.addWidget(btn1,0,2)

btn2 = QPushButton('close_serial')
btn2.clicked.connect(close_serial) 
layout.addWidget(btn2,0,3)

led1 = QLed(onColour=QLed.Yellow, shape=QLed.Round)
led1.value = False
layout.addWidget(led1)

btn10 = QPushButton('open1')
btn10.clicked.connect(open1) 
layout.addWidget(btn10)

btn11 = QPushButton('close1')
btn11.clicked.connect(close1) 
layout.addWidget(btn11)

btn12 = QPushButton('device1 name')
btn12.clicked.connect(name1) 
layout.addWidget(btn12)

led2 = QLed(onColour=QLed.Yellow, shape=QLed.Round)
led2.value = False
layout.addWidget(led2)

btn20 = QPushButton('open2')
btn20.clicked.connect(open2) 
layout.addWidget(btn20)

btn21 = QPushButton('close2')
btn21.clicked.connect(close2) 
layout.addWidget(btn21)

btn22 = QPushButton('device2 name')
btn22.clicked.connect(name2) 
layout.addWidget(btn22)

led3 = QLed(onColour=QLed.Yellow, shape=QLed.Round)
led3.value = False
layout.addWidget(led3)

btn30 = QPushButton('open3')
btn30.clicked.connect(open3) 
layout.addWidget(btn30)

btn31 = QPushButton('close3')
btn31.clicked.connect(close3) 
layout.addWidget(btn31)

btn32 = QPushButton('device3 name')
btn32.clicked.connect(name3) 
layout.addWidget(btn32)

led4 = QLed(onColour=QLed.Yellow, shape=QLed.Round)
led4.value = False
layout.addWidget(led4)

btn40 = QPushButton('open4')
btn40.clicked.connect(open4) 
layout.addWidget(btn40)

btn41 = QPushButton('close4')
btn41.clicked.connect(close4) 
layout.addWidget(btn41)

btn42 = QPushButton('device4 name')
btn42.clicked.connect(name4) 
layout.addWidget(btn42)

window.setLayout(layout)
window.show()
sys.exit(app.exec_())