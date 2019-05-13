#include <Arduino.h>
/* Here ESP32 will keep 2 roles:
1/ read data from DHT11/DHT22 sensor
2/ control led on-off
So it willpublish temperature topic and scribe topic bulb on/off
*/
#include <Adafruit_Sensor.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <stdio.h>

/* change it with your ssid-password */
// const char* ssid = "dd-wrt";
// const char* password = "0000000000";

#define WIFI_SSID "ProteinLab_3D"
#define WIFI_PASSWORD "protein-dis3d"
/***************Factores para Sleep*******************************************/
#define uS_TO_S_FACTOR 1000000  /* Conversion factor for micro seconds to seconds */
#define TIME_TO_SLEEP  3000        /* Time ESP32 will go to sleep (in seconds) */

/* this is the IP of PC/raspberry where you installed MQTT Server
on Wins use "ipconfig"
on Linux use "ifconfig" to get its IP address */
const char* mqtt_server = "192.168.1.123";

/* define DHT pins */
#define DHTPIN 14
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);
float temperatura = 0;
float humedad = 0;

/* create an instance of PubSubClient client */
WiFiClient espClient;
PubSubClient client(espClient);

/*LED GPIO pin*/
const char led = 12;

/* topics */
#define TOPIC    "proteinlab/design/id1"
// #define HUM_TOPIC     "dato/esp32_01/hum"

long lastMsg = 0;
char msg[10];
char mt[9];
char mh[9];

void receivedCallback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message received: ");
  Serial.println(topic);

  Serial.print("payload: ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
  /* we got '1' -> on */
  if ((char)payload[0] == '1') {
    digitalWrite(led, HIGH);
  } else {
    /* we got '0' -> on */
    digitalWrite(led, LOW);
  }

}

void mqttconnect() {
  /* Loop until reconnected */
  while (!client.connected()) {
    Serial.print("MQTT connecting ...");
    /* client ID */
    String clientId = "ESP32Client";
    /* connect now */
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      /* subscribe topic with default QoS 0*/
      //client.subscribe(LED_TOPIC);
    } else {
      Serial.print("failed, status code =");
      Serial.print(client.state());
      Serial.println("try again in 5 seconds");
      /* Wait 5 seconds before retrying */
      delay(5000);
    }
  }
  Serial.print("YA se conecto a MQTT");
}

void setup()
{
  Serial.begin(115200);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(WIFI_SSID);

  //WiFi.begin(ssid, password);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  /* set led as output to control led on-off */
  pinMode(led, OUTPUT);

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  /* configure the MQTT server with IPaddress and port */
  client.setServer(mqtt_server, 1883);
  /* this receivedCallback function will be invoked
  when client received subscribed topic */
  client.setCallback(receivedCallback);
  /*start DHT sensor */
  dht.begin();
  Serial.print("YA configuro DHT");

  esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR);
  Serial.print("Luego del sleep enable");
  delay(500);

}
void loop()
{
  Serial.print("Entro al loop");
  /* if client was disconnected then try to reconnect again */
  if (!client.connected())
  {
    Serial.print("No esta concetado a mqtt en el loop");
    mqttconnect();
    Serial.print("Ya se conecto en el loop");
  }
  /* this function will listen for incomming
  subscribed topic-process-invoke receivedCallback */
  client.loop();
  /* we measure temperature every 3 secs
  we count until 3 secs reached to avoid blocking program if using delay()*/
  long now = millis();
  Serial.print(now);
  if (now - lastMsg > 3000)
  {
    Serial.print("Entro despues de dormir");
    lastMsg = now;
    /* read DHT11/DHT22 sensor and convert to string */
    temperatura = dht.readTemperature();
    humedad = dht.readHumidity();
    if (!isnan(temperatura))
    {
      Serial.println("Obteniendo datos");
      // snprintf (mt, 5, "%f", temperatura);
      // snprintf (mh, 5, "%f", humedad);
      snprintf (msg, 10, "%.1f/%.1f", temperatura, humedad);
      Serial.println("Se genera string");
      // strcat(msg,mt);
      // Serial.println("------");
      // Serial.print(msg);
      // strcat(msg,"/");
      // Serial.println("------");
      // Serial.print(msg);  
      // strcat(msg,mh);
      // Serial.println("------");
      // Serial.print(msg);
      Serial.print("El mensaje es: ");
      Serial.print( msg);
      /* publish the message */
      client.publish(TOPIC, msg);
      Serial.print("Se publico por mqtt");
    }
    // if (!isnan(humedad))
    // {
    //   snprintf (msg, 20, "%lf", humedad);
    //   /* publish the message */
    //   client.publish(HUM_TOPIC, msg);
    // }
  }
  Serial.print("Se va a dormir");
  // esp_deep_sleep_start();
  delay(5000);
}
