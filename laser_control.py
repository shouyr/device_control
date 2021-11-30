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
    ser = serial.Serial(comstr[0:4], 9600, timeout=0.04)
    if ser.isOpen() == True:
        led.value = True

def close_serial():
    ser.close()
    led.value = ser.isOpen()
def selectionchange():
    led.value = False

def refreshdata():
    if led.value == True:
        ser.write(b'\x7E\x50\x01\x01\x00')
        res1 = ser.readline().hex()
        if res1[-1] == '1':
            led1.value = True
        else: 
            led1.value = False
        ser.write(b'\x7E\x52\x01\x01\x00')
        res2 = ser.readline().hex()
        respower = str(int('0x'+res2[8:12], 16))
        lab4.setText(respower+' mW')
        ser.write(b'\x7E\x53\x01\x01\x00')
        res3 = ser.readline().hex()
        restemp = str(round(int('0x'+res3[8:12], 16)*0.1,2))
        lab2.setText(restemp+' °C')
                
            
def open1():
    ser.write(b'\x7E\x04\x01\x02\x00\x00')
    res = ser.readline().hex()
    ser.write(b'\x7E\x02\x01\x01\x01')
    res = ser.readline().hex()
    ser.write(b'\x7E\x53\x01\x01\x00')
    res1 = ser.readline().hex()
    if len(res1) != 12:
        alert = QMessageBox()
        alert.setText('Is remote mode on? Check the control box.')
        alert.exec()
    refreshdata()
    
def close1():
    ser.write(b'\x7E\x02\x01\x01\x00')
    res = ser.readline().hex()
    refreshdata()

def vc1():
    vslid1 = slid1.value()
    lab5.setText(str(vslid1)+' mW')

def vc2():
    vslid2 = slid2.value()
    lab6.setText(str(vslid2)+' s')
    
def setpower():
    power = slid1.value()
    ser.write(b'\x7E\x04\x01\x02'+power.to_bytes(2, byteorder="big"))
    res = ser.readline().hex()
    refreshdata()
    
def startheat():
    tt = slid2.value()
    setpower()
    ser.write(b'\x7E\x02\x01\x01\x01')
    res = ser.readline().hex()
    ser.write(b'\x7E\x53\x01\x01\x00')
    res1 = ser.readline().hex()
    if len(res1) != 12:
        alert = QMessageBox()
        alert.setText('Is remote mode on? Check the control box.')
        alert.exec()
    refreshdata()
    timer2 = QTimer()
    timer2.singleShot(1000*tt,close1)


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
window.setWindowTitle('Diode Laser')
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
layout.addWidget(led1,1,1)

btn10 = QPushButton('turn on')
btn10.clicked.connect(open1) 
layout.addWidget(btn10,1,2)

btn11 = QPushButton('turn off')
btn11.clicked.connect(close1) 
layout.addWidget(btn11,1,3)

lab1 = QLabel("Temperature")
lab1.setAlignment(Qt.AlignRight)
layout.addWidget(lab1,2,0)
lab2 = QLabel("    °C")
#lab2.setFrameStyle(QFrame.Panel)
layout.addWidget(lab2,2,1)
lab3 = QLabel("Power")
lab3.setAlignment(Qt.AlignRight)
layout.addWidget(lab3,2,2)
lab4 = QLabel("    mW")
layout.addWidget(lab4,2,3)

slid1 = QSlider(Qt.Horizontal)
slid1.setMinimum(0) 
slid1.setMaximum(9999) 
slid1.setValue(0)  
slid1.valueChanged.connect(vc1)
layout.addWidget(slid1,3,0,1,2)
lab5 = QLabel('power:'+str(slid1.value())+' W')
layout.addWidget(lab5,3,2)
btn5 = QPushButton('Set power')
btn5.clicked.connect(setpower) 
layout.addWidget(btn5,3,3)


slid2 = QSlider(Qt.Horizontal)
slid2.setMinimum(1) 
slid2.setMaximum(120) 
slid2.setValue(50) 
slid2.valueChanged.connect(vc2)
layout.addWidget(slid2,4,0,1,2)
lab6 = QLabel("heating "+str(slid2.value())+' s')
layout.addWidget(lab6,4,2)
btn6 = QPushButton('Start heating')
btn6.clicked.connect(startheat) 
layout.addWidget(btn6,4,3)

btn7 = QPushButton('exit')
btn7.clicked.connect(quit1) 
layout.addWidget(btn7,5,3)

timer = QTimer()  # set up your QTimer
timer.timeout.connect(refreshdata)  # connect it to your update function
timer.start(10000)  # set it to timeout in 10000 ms

window.setLayout(layout)
window.show()
sys.exit(app.exec_())
