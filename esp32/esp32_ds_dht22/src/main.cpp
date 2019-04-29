#include <Arduino.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
//Firebase.h incluye la libreria WiFi.h
#include <FirebaseESP32.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

#define FIREBASE_HOST "https://construccion-30739.firebaseio.com/"
#define FIREBASE_AUTH "Db4uGKvMYUmY6F6Nn5tBQvuDesGxxhLZUCTj0D4y"
#define WIFI_SSID "LabProtein"
#define WIFI_PASSWORD "teinpro_bal1602"
/***************Factores para Sleep*******************************************/
#define uS_TO_S_FACTOR 1000000  /* Conversion factor for micro seconds to seconds */
#define TIME_TO_SLEEP  3        /* Time ESP32 will go to sleep (in seconds) */

/************************Sensor de temperatura y humedad*****************************/
#define DHTPIN		26		//pin de conexion
#define DHTTYPE		DHT22	//tipo aplicado

/*************************** Inicializaci�n DHT ************************/
DHT dht (DHTPIN, DHTTYPE);
// Connect pin 1 (on the left) of the sensor to +5V
// NOTE: If using a board with 3.3V logic like an Arduino Due connect pin 1
// to 3.3V instead of 5V!
// Connect pin 2 of the sensor to whatever your DHTPIN is
// Connect pin 4 (on the right) of the sensor to GROUND
// Connect a 10K resistor from pin 2 (data) to pin 1 (power) of the sensor

//Servidor de tiempo
WiFiUDP ntpUDP;
// By default 'pool.ntp.org' is used with 60 seconds update interval and
// no offset
NTPClient timeClient(ntpUDP,"ntp.shoa.cl");

void streamCallback(streamResult event)
{
  String eventType = event.eventType();
  eventType.toLowerCase();
  if(eventType == "put")
  {
    Serial.println("The stream event path: " + event.path() + ", value: " + String(event.getFloat()));
    Serial.println();
  }
}

// double randomDouble(double minf, double maxf)
// {
//   return minf + random(1UL << 31) * (maxf - minf) / (1UL << 31);  // use 1ULL<<63 for max double values)
// }


void setup() {

  delay(2000);		//Estabilizaci�n del sistema, requerido para DHT22
  dht.begin();
  Serial.begin(115200);
  while (!Serial);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(300);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());

  timeClient.begin();

  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  Firebase.stream("/dht22", streamCallback());

  esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR);
}

void loop()
{
  timeClient.update();
  String fechora = timeClient.getFormattedDate();
  Serial.println(timeClient.getFormattedDate());

  float h = dht.readHumidity();
  float t = dht.readTemperature();
  //Envio de humedad
  if(h==h)
  {
    Serial.println("Set float value: " + String(h) + " to /dht22/hum/sensorValue");
    Firebase.setFloat("/dht22/"+fechora+"/hum/sensorValue", h );
  }

  //Envio de temperatura
  if(t==t)
  {
    Serial.println("Set float value: " + String(t) + " to /dht22/temp/sensorValue");
    Firebase.setFloat("/dht22/"+fechora+"/temp/sensorValue", t );
  }
  delay(2000);
  esp_deep_sleep_start();
}
