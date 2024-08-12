#include "DHT.h"
#define DHTPIN1 23  // Digital pin connected to the DHT sensor
#define DHTPIN2 25
#define DHTPIN3 31


//#define DHTTYPE DHT11   // DHT 11
#define DHTTYPE DHT11  // DHT 22  (AM2302), AM2321
//#define DHTTYPE DHT21   // DHT 21 (AM2301)


DHT dht1(DHTPIN1, DHTTYPE);
DHT dht2(DHTPIN2, DHTTYPE);
DHT dht3(DHTPIN3, DHTTYPE);

void initDHT() {
  delay(500);
  dht1.begin();
  dht2.begin();
  dht3.begin();
  
}



/*
  Function/Method for getting DHT temperature
  
*/
float getDHTTemperature1(boolean isFarenheit) {
  float temperature;
  if (isFarenheit) {
    temperature = dht1.readTemperature(true);
  } else {
    temperature = dht1.readTemperature();
  }
  if (isnan(temperature)) return -1;
  else return temperature;
}


/*
  Function/Method for getting DHT humidity
*/
float getDHTHumidity1() {
  float humidity = dht1.readHumidity();
  if (isnan(humidity)) return -1;
  else return humidity;
}

float getDHTTemperature2(boolean isFarenheit) {
  float temperature;
  if (isFarenheit) {
    temperature = dht2.readTemperature(true);
  } else {
    temperature = dht2.readTemperature();
  }
  if (isnan(temperature)) return -1;
  else return temperature;
}


/*
  Function/Method for getting DHT humidity
*/
float getDHTHumidity2() {
  float humidity = dht2.readHumidity();
  if (isnan(humidity)) return -1;
  else return humidity;
}





float getDHTTemperature3(boolean isFarenheit) {
  float temperature;
  if (isFarenheit) {
    temperature = dht3.readTemperature(true);
  } else {
    temperature = dht3.readTemperature();
  }
  if (isnan(temperature)) return -1;
  else return temperature;
}


/*
  Function/Method for getting DHT humidity
*/
float getDHTHumidity3() {
  float humidity = dht3.readHumidity();
  if (isnan(humidity)) return -1;
  else return humidity;
}