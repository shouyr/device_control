from PyQt5.QtWidgets import (QApplication, QPushButton, QWidget, QGridLayout, QComboBox,  QInputDialog, QMessageBox)
from QLed import QLed
import serial
import serial.tools.list_ports
import sys
from os.path import exists

def selectionchange():
    led.value = False
def oepn_serial():
    global ser
    comstr = cb.currentText()
    ser = serial.Serial(comstr[0:4], 9600, timeout=1)
    if ser.isOpen() == True:
        led.value = True
        ser.write(b'\x55\x56\x00\x00\x00\x00\x08\xB3') #close all 
        led1.value = False
        led2.value = False
        led3.value = False
        led4.value = False
        led5.value = False
        led6.value = False
        led7.value = False
        led8.value = False
    else:
        alert = QMessageBox()
        alert.setText('serial problem')
        alert.exec()
        led.value = False
   # return ser
def close_serial():
    ser.close()
    led.value = ser.isOpen()
    

def open1():
    ser.write(b'\x55\x56\x00\x00\x00\x01\x01\xAD')
    led1.value = True
def close1():
    ser.write(b'\x55\x56\x00\x00\x00\x01\x02\xAE') 
    led1.value = False
def name1():
    text, ok = QInputDialog.getText(window, 'name', 'input the name')
    if ok:
        btn12.setText(text)
        name_list[0] = text
        f = open('name_list.txt','w')
        for i in range(8):
            f.writelines(name_list[i]+'\n')
        f.close() 
def open2():
    ser.write(b'\x55\x56\x00\x00\x00\x02\x01\xAE')
    led2.value = True
def close2():
    ser.write(b'\x55\x56\x00\x00\x00\x02\x02\xAF') 
    led2.value = False
def name2():
    text, ok = QInputDialog.getText(window, 'name', 'input the name')
    if ok:
        btn22.setText(text) 
        name_list[1] = text
        f = open('name_list.txt','w')
        for i in range(8):
            f.writelines(name_list[i]+'\n')
        f.close() 
def open3():
    ser.write(b'\x55\x56\x00\x00\x00\x03\x01\xAF')
    led3.value = True
def close3():
    ser.write(b'\x55\x56\x00\x00\x00\x03\x02\xB0') 
    led3.value = False
def name3():
    text, ok = QInputDialog.getText(window, 'name', 'input the name')
    if ok:
        btn32.setText(text)
        name_list[2] = text
        f = open('name_list.txt','w')
        for i in range(8):
            f.writelines(name_list[i]+'\n')
        f.close() 
def open4():
    ser.write(b'\x55\x56\x00\x00\x00\x04\x01\xB0')
    led4.value = True
def close4():
    ser.write(b'\x55\x56\x00\x00\x00\x04\x02\xB1') 
    led4.value = False
def name4():
    text, ok = QInputDialog.getText(window, 'name', 'input the name')
    if ok:
        btn42.setText(text)
        name_list[3] = text
        f = open('name_list.txt','w')
        for i in range(8):
            f.writelines(name_list[i]+'\n')
        f.close() 
def open5():
    ser.write(b'\x55\x56\x00\x00\x00\x05\x01\xB1')
    led5.value = True
def close5():
    ser.write(b'\x55\x56\x00\x00\x00\x05\x02\xB2') 
    led5.value = False
def name5():
    text, ok = QInputDialog.getText(window, 'name', 'input the name')
    if ok:
        btn52.setText(text)
        name_list[4] = text
        f = open('name_list.txt','w')
        for i in range(8):
            f.writelines(name_list[i]+'\n')
        f.close() 
def open6():
    ser.write(b'\x55\x56\x00\x00\x00\x06\x01\xB2')
    led6.value = True
def close6():
    ser.write(b'\x55\x56\x00\x00\x00\x06\x02\xB3') 
    led6.value = False
def name6():
    text, ok = QInputDialog.getText(window, 'name', 'input the name')
    if ok:
        btn42.setText(text)
        name_list[5] = text
        f = open('name_list.txt','w')
        for i in range(8):
            f.writelines(name_list[i]+'\n')
        f.close() 
def open7():
    ser.write(b'\x55\x56\x00\x00\x00\x07\x01\xB3')
    led7.value = True
def close7():
    ser.write(b'\x55\x56\x00\x00\x00\x07\x02\xB4') 
    led7.value = False
def name7():
    text, ok = QInputDialog.getText(window, 'name', 'input the name')
    if ok:
        btn42.setText(text)
        name_list[6] = text
        f = open('name_list.txt','w')
        for i in range(8):
            f.writelines(name_list[i]+'\n')
        f.close() 
def open8():
    ser.write(b'\x55\x56\x00\x00\x00\x08\x01\xB4')
    led8.value = True
def close8():
    ser.write(b'\x55\x56\x00\x00\x00\x08\x02\xB5') 
    led8.value = False
def name8():
    text, ok = QInputDialog.getText(window, 'name', 'input the name')
    if ok:
        btn42.setText(text)
        name_list[7] = text
        f = open('name_list.txt','w')
        for i in range(8):
            f.writelines(name_list[i]+'\n')
        f.close() 
def quit1():
    sys.exit()




if exists('name_list.txt'):
    f = open('name_list.txt','r')
    name_list = f.read().splitlines()
    f.close()  
else:
    name_list = ['device1_name','device2_name','device3_name','device4_name','device5_name','device6_name','device7_name','device8_name']
    f = open('name_list.txt','w')
    for i in range(8):
        f.writelines(name_list[i]+'\n')
    f.close() 
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

btn12 = QPushButton(name_list[0])
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

btn22 = QPushButton(name_list[1])
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

btn32 = QPushButton(name_list[2])
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

btn42 = QPushButton(name_list[3])
btn42.clicked.connect(name4) 
layout.addWidget(btn42)

led5 = QLed(onColour=QLed.Yellow, shape=QLed.Round)
led5.value = False
layout.addWidget(led5)

btn50 = QPushButton('open5')
btn50.clicked.connect(open5) 
layout.addWidget(btn50)

btn51 = QPushButton('close5')
btn51.clicked.connect(close5) 
layout.addWidget(btn51)

btn52 = QPushButton(name_list[4])
btn52.clicked.connect(name5) 
layout.addWidget(btn52)

led6 = QLed(onColour=QLed.Yellow, shape=QLed.Round)
led6.value = False
layout.addWidget(led6)

btn60 = QPushButton('open6')
btn60.clicked.connect(open6) 
layout.addWidget(btn60)

btn61 = QPushButton('close6')
btn61.clicked.connect(close6) 
layout.addWidget(btn61)

btn62 = QPushButton(name_list[5])
btn62.clicked.connect(name6) 
layout.addWidget(btn62)

led7 = QLed(onColour=QLed.Yellow, shape=QLed.Round)
led7.value = False
layout.addWidget(led7)

btn70 = QPushButton('open7')
btn70.clicked.connect(open7) 
layout.addWidget(btn70)

btn71 = QPushButton('close7')
btn71.clicked.connect(close7) 
layout.addWidget(btn71)

btn72 = QPushButton(name_list[6])
btn72.clicked.connect(name7) 
layout.addWidget(btn72)

led8 = QLed(onColour=QLed.Yellow, shape=QLed.Round)
led8.value = False
layout.addWidget(led8)

btn80 = QPushButton('open8')
btn80.clicked.connect(open8) 
layout.addWidget(btn80)

btn81 = QPushButton('close8')
btn81.clicked.connect(close8) 
layout.addWidget(btn81)

btn82 = QPushButton(name_list[7])
btn82.clicked.connect(name8) 
layout.addWidget(btn82)

btn9 = QPushButton('exit')
btn9.clicked.connect(quit1) 
layout.addWidget(btn9)

window.setLayout(layout)
window.show()
sys.exit(app.exec_())
