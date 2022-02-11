#include <Servo.h>

int potPin = 0;
int servoPin = 9;
int servoPin2 = 10;
Servo servo; 
Servo servo2; 

int nSwitch = 0;
int nAngle = 0;
  
void setup() 
{ 
  Serial.begin(9600);
  pinMode(servoPin, OUTPUT);
  pinMode(servoPin2, OUTPUT);
  servo.attach(servoPin);
  servo2.attach(servoPin2);
} 

void loop() 
{ 
  if(Serial.available())
  {
    nSwitch = Serial.read();
  }
  switch(nSwitch)
  {
    case '0':
      nAngle = 0;
      servo.write(nAngle); 
      break;
    case '1':
      nAngle = 45;
      servo.write(nAngle); 
      break;
    case '2':
      nAngle = 0;
      servo2.write(nAngle);
      break;
    case '3':
      nAngle = 45;
      servo2.write(nAngle); 
      break;
    default:
      break;
  }
  delay(500);
} 
