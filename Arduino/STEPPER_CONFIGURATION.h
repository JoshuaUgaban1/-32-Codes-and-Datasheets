// Define the pins
const int PUL = 7;  // Pulse pin
const int DIR = 2;  // Direction pin
const int ENA = 4;  // Enable pin

void initSTEPPER() {
  // Set the pin modes
  pinMode(PUL, OUTPUT);
  pinMode(DIR, OUTPUT);
  pinMode(ENA, OUTPUT);
  
  // Enable the motor driver
  digitalWrite(ENA, LOW);
}

void weqw(int rpm) {
  // Set the direction (1 for clockwise, 0 for counterclockwise)
  digitalWrite(DIR, HIGH); // Change this if you want to change direction
  
  // Step the motor
  for (int i = 0; i < 200; i++) { // 200 steps is one full revolution for most NEMA 17 motors
    digitalWrite(PUL, HIGH);
    delayMicroseconds(500); // Adjust this delay as needed for your motor speed
    digitalWrite(PUL, LOW);
    delayMicroseconds(500); // Adjust this delay as needed for your motor speed
  }
  
  // Delay before changing direction (if needed)
  delay(1000); // Adjust this delay as needed
  
  // Set the direction (0 for counterclockwise, 1 for clockwise)
  //digitalWrite(DIR, LOW); // Change this if you want to change direction
  
  // Step the motor
  // for (int i = 0; i < 200; i++) {
  //   digitalWrite(PUL, HIGH);
  //   delayMicroseconds(500); // Adjust this delay as needed for your motor speed
  //   digitalWrite(PUL, LOW);
  //   delayMicroseconds(500); // Adjust this delay as needed for your motor speed
  // }
  
  // // Delay before repeating
  // delay(1000); // Adjust this delay as needed
}

void operateTB6600Ccw(float targetRPM) {
  digitalWrite(DIR, HIGH);  // LEFT
  int steps = 400;
  float delayBetweenSteps = 60000000.0 / (targetRPM * steps);

 
    digitalWrite(PUL, HIGH);
    delayMicroseconds(delayBetweenSteps);
    digitalWrite(PUL, LOW);
    delayMicroseconds(delayBetweenSteps);
  
}
