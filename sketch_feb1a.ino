#include "DHT.h"
#include <Servo.h>

Servo servo1;
Servo servo2;
int fanPin = 11;
int humidPin = A0;
int pR1 = A1;
int pR2 = A2;
int pot = A3;
int soilPin = A4;
float temperature = 0;
float humidity = 0;

int dayThreshold = 200;
int nightThreshold = 0;

int lightIn = 0;
int lightOut;
int potRead = 0;
int soilRead = 0;

int plantType = 0;
float watering = 0;
float sunlight = 0;

#define DHTPIN humidPin
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);




void setup() {  // put your setup code here, to run once:
  Serial.begin(9600);
  dht.begin();
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
  pinMode(A3, INPUT);
  pinMode(A4, INPUT);
  servo1.attach(9);
  servo2.attach(10);
}

void waterOn() {
  servo2.write(0);
}

void waterOff() {
  servo2.write(180);
}

void fanSpeed(int percent) {
  percent = 0.5*percent/100*1023;
  analogWrite(fanPin, percent);
}

void getSensorData() {
  humidity = dht.readHumidity();
  temperature = dht.readTemperature(); //Celsius. Add true if farenheit
  lightIn = analogRead(pR1);
  lightOut = analogRead(pR2);
  potRead = analogRead(pot);
  soilRead = analogRead(soilPin);
  plantType = map(potRead, 0, 1000, 1, 9);
  Serial.println("Humidity: " + String(humidity)); 
  Serial.println("Temperature: " + String(temperature)); 
  Serial.println("Light Inside: " + String(lightIn)); 
  Serial.println("Light Outside: " + String(lightOut)); 
  Serial.println("Potentiometer: " + String(potRead));
  Serial.println("Plant Type" + String(plantType)); 
  Serial.println("Soil: " + String(soilPin)); 
}

void sortPlant() {
  switch (plantType) {
    case 1:
    watering = 0;
    sunlight = 0;
    break;
    case 2:
    watering = 0;
    sunlight = 0.85;
    break;
    case 3:
    watering = 0;
    sunlight =1;
    break;

    case 4:
    watering = 0.50;
    sunlight = 0.85;
    break;
    case 5:
    watering = 0.50;
    sunlight = 0.85;
    break;
    case 6:
    watering = 0.5;
    sunlight =1;
    break;

    case 7:
    watering = 1;
    sunlight = 0;
    break;
    case 8:
    watering = 1;
    sunlight = 0.85;
    break;
    case 9:
    watering = 1;
    sunlight =1;
    break;


  }
}

void setLid(int percent) {
  //percent = (percent/100)*180;
  percent = sunlight*percent;
  percent = 180-percent;
  servo1.write(percent);
  if (sunlight == 0) {servo1.write(90);}
  delay (2000);
  Serial.println("Hello "+ String(lightOut));


}

void loop() {
  
  // put your main code here, to run repeatedly:
  getSensorData();
  sortPlant();
  Serial.println();
  Serial.println("Plant Type: " + String(plantType));
  Serial.println("Sunlight " + String(sunlight));
  Serial.println("Watering: " + String(watering));
  delay(1000);
    int i = 0;
    if (lightOut >= dayThreshold){
      //servo1.write(80);
      setLid(180);
    }
    while (i < 7 && lightOut >= dayThreshold) {
      delay (1000);
      getSensorData();
      i = i+1;
      
      }
    if (lightOut <= dayThreshold) {
        servo1.write(90);
        delay(2000);
        getSensorData();
        
  }

  
  

}