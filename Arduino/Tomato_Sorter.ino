
float CURRENT_TEMPERATURE_1;
float CURRENT_TEMPERATURE_2;
float CURRENT_TEMPERATURE_3;


#include "LIB.h"
#include "SERVO_CONFIG.h"
#include "STEPPER_CONFIG.h"
#include "L298N_CONFIG.h"
#include "DHT_CONFIG.h"
#include "RELAY_CONFIG.h"

bool isSorter1Open = false;
bool isSorter2Open = false;
bool isSorter3Open = false;

int RUN_DISPENSER = -1;
int DISPENSER_INTERVAL = 1;
unsigned long DISPENSER_TIME_FOR_INTERVAL;

int RUN_PRESERVATION = -1;


unsigned long time_for_interval;
int loop_interval = 1000;
void setup() {
  Serial.begin(9600);

  initSERVO();
  initSTEPPER();
  initL298N();
  initRELAY();
  initDHT();
  Serial.println("Tomato Sorter - Arduino Starting!");
}

void loop() {

  if (Serial.available() > 0) {
    String incoming_command;
    Serial.println("Received");
    String command;
    String pi_data;
    String pi_data_value;

    incoming_command = Serial.readStringUntil('\n');
    
    Serial.println(incoming_command);
    incoming_command.trim();
    command = split(incoming_command, ':', 0);
    pi_data = split(incoming_command, ':', 1);

    if (command == "operate-dispenser") {
      String dispense = pi_data;
      
      if(dispense == "true"){
        RUN_DISPENSER = 1; // start dispenser

        
        operateSorter1(90);
        operateGate(40);
        
        Serial.println("Dispensing Tomato!"); 
      }else if(dispense == "false"){
        RUN_DISPENSER = 0; // stop dispenser 
        
        Serial.println("Stopping dispenser!");
      }
      
    } else if (command == "operate-conveyor") {
      
      operateL298NMotor(300);

    } else if (command == "stop-conveyor") {
      RUN_DISPENSER = 0; // stop dispenser 
      stopL298NMotor();

    } 
    
    else if (command == "operate-sorter-1") {
      operateGate(90);
      int angle = pi_data.toInt();
      
      operateSorter1(35);

    } else if (command == "operate-sorter-2") {
      operateGate(90);
      
      int angle = pi_data.toInt();
      operateSorter1(90);
      operateSorter2(115);

      
    } else if (command == "operate-sorter-3") {

      operateGate(90);
      int angle = pi_data.toInt();

      operateSorter1(90); // close sorter 1
      operateSorter2(70);   // close sorter 2
      operateSorter3(123);

    } else if (command == "close-sorter") {
      
      operateGate(90);

      closeSorter();

    } else if (command == "operate-gate-open"){
       int angle = pi_data.toInt();
       operateGate(angle);

       //operateGate(180);
     
    } else if (command == "operate-gate-close"){
       int angle = pi_data.toInt();
       operateGate(angle);

       
    } else if (command == "operate-preservation") {
      String preserve = pi_data;
      
      if(preserve == "true"){
        RUN_PRESERVATION = 1; // start preservation

        operateRELAY(RELAY_1,  true);
        operateRELAY(RELAY_2,  true);
        operateRELAY(RELAY_3,  true);
        
        Serial.println("Preserving Tomato!"); 
      }else if(preserve == "false"){
        RUN_PRESERVATION = 0; // stop preservation 
        operateRELAY(RELAY_1,  false);
        operateRELAY(RELAY_2,  false);
        operateRELAY(RELAY_3,  false);
        Serial.println("Stopping preservation!");
      }

    } else if(command == "stop"){
      RUN_DISPENSER = 0;
      RUN_PRESERVATION = 0;
      operateGate(40);
      stopL298NMotor();
    }
    
  }



   if (millis() - time_for_interval > loop_interval) {
    time_for_interval = millis();

    if(RUN_PRESERVATION == 1){
      float temp1 = getDHTTemperature1(false);
      float temp2 = getDHTTemperature2(false);
      float temp3 = getDHTTemperature3(false);

      if(temp1 > 13.75){
        operateRELAY(RELAY_1, true);
      }else{
        operateRELAY(RELAY_1, false);
      }

      if(temp2 > 11.75){
        operateRELAY(RELAY_2, true);
      }else{
        operateRELAY(RELAY_2, false);
      }

      if(temp3 > 8.5){
        operateRELAY(RELAY_3, true);
      }else{
        operateRELAY(RELAY_3, false);
      }


      Serial.print("REF:");
      Serial.print(temp1);
      Serial.print(":");
      Serial.print(temp2);
      Serial.print(":");
      Serial.println(temp3);
    
    }  
   }


   if (RUN_DISPENSER == 1) {
//     if (millis() - DISPENSER_TIME_FOR_INTERVAL > DISPENSER_INTERVAL) {
//       DISPENSER_TIME_FOR_INTERVAL = millis();
//       Serial.println("RUNNNG");
//       
//     }
      operateTB6600Ccw(100);
      operateL298NMotor(200);
      
   }

   //  operateSorter1(35);
   //  operateSorter2(115);
   //  operateSorter3(123);
   //  operateGate(180);

   
 
}
