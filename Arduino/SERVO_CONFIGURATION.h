#include <Servo.h>

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;

void moveServoToAngle(Servo& servo, int targetAngle, int stepDelay = 3) {
  int currentAngle = servo.read();
  
  // Determine the direction to move the servo
  int increment = (currentAngle < targetAngle) ? 1 : -1;

  // Move the servo gradually to the target angle
  while (currentAngle != targetAngle) {
    currentAngle += increment;
    servo.write(currentAngle);
    delay(stepDelay);
  }
}

void initSERVO() {
  // Attach servos to pins
  servo1.attach(44);  
  servo2.attach(45); 
  servo3.attach(46);
  servo4.attach(11);
  moveServoToAngle(servo1, 70);
  moveServoToAngle(servo2, 160);
  moveServoToAngle(servo3, 90);
  moveServoToAngle(servo4, 40);
}

void operateSorter(int angle) {
  moveServoToAngle(servo1, 0);
  moveServoToAngle(servo1, angle);
  
}



void operateRotator(int angle) {
  moveServoToAngle(servo2, 0);
  moveServoToAngle(servo3, 0);
  moveServoToAngle(servo2, angle);
  moveServoToAngle(servo3, angle);
  
}

void operateSorter1(int angle) {
  
  moveServoToAngle(servo3, angle);
  //delay(1000);
  //moveServoToAngle(servo3, 90);
  
}

void operateSorter2(int angle) {
  moveServoToAngle(servo1, angle);
  //delay(1000);
  //moveServoToAngle(servo1, 70);
}

void operateSorter3(int angle) {
  
  moveServoToAngle(servo2, angle);
  //delay(1000);
  //moveServoToAngle(servo2, 160);
  //
}

void operateGate(int angle){
  moveServoToAngle(servo4, angle);
//  delay(1000);
//  moveServoToAngle(servo4, 40);
}

void closeSorter(){
  //Serial.println("Closing sorter");
  moveServoToAngle(servo1, 70);
  moveServoToAngle(servo2, 160);
  moveServoToAngle(servo3, 90);
}
