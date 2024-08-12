// Pin definitions
#define L298N_ENB 10
#define L298N_IN4 9
#define L298N_IN3 8
#define L298N_IN2 6
#define L298N_IN1 5
#define L298N_ENA 3

void initL298N() {
  
   //pinMode(L298N_ENA, OUTPUT);
   //pinMode(L298N_IN1, OUTPUT);
   //pinMode(L298N_IN2, OUTPUT);
   pinMode(L298N_IN3, OUTPUT);
   pinMode(L298N_IN4, OUTPUT);
   pinMode(L298N_ENB, OUTPUT);
}

// Function to control the motor speed
void controlMotorSpeed(int speed) {
  // Clamp the speed value between -255 and 255
  speed = constrain(speed, -255, 255);

  // Set the direction based on the sign of the speed
  if (speed >= 0) {
    //digitalWrite(L298N_IN1, HIGH);
    //digitalWrite(L298N_IN2, LOW);
    digitalWrite(L298N_IN3, LOW);
    digitalWrite(L298N_IN4, HIGH);
  } else {
    //digitalWrite(L298N_IN1, LOW);
    //digitalWrite(L298N_IN2, HIGH);
    digitalWrite(L298N_IN3, HIGH);
    digitalWrite(L298N_IN4, LOW);
    speed = -speed; // Make the speed positive for analogWrite
  }

  // Set the motor speed using PWM
  analogWrite(L298N_ENA, speed);
  analogWrite(L298N_ENB, speed);
}

void operateL298NMotor(int speed) {
  digitalWrite(L298N_ENB, HIGH);  // Start Motor B
  controlMotorSpeed(speed); 

}

void stopL298NMotor() {
  digitalWrite(L298N_ENB, LOW);  // Stop motor B
}
