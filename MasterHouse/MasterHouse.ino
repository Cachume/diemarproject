#include <Servo.h>
#include <DHT.h>
#include <DHT_U.h>

int luces[] = {13, 12, 11, 10, 7, 6, 9};
int estadoluces[] = {0, 0, 0, 0, 0, 0, 0};
bool modoAutomatico = false;
int pirPin = 4;
int pirState = LOW;
Servo Garage;
bool estado_garage = false;

#define DHTPIN 5      // Pin al que está conectado el sensor
#define DHTTYPE DHT22 // Tipo de sensor DHT11
#define PIN_MQ2 A1 //Pin al que esta conectado el sensor de humo y gas

// RemoteXY select connection mode and include
#define REMOTEXY_MODE__ESP8266_SOFTSERIAL_POINT

#include <SoftwareSerial.h>

// RemoteXY connection settings 
#define REMOTEXY_SERIAL_RX 2
#define REMOTEXY_SERIAL_TX 3
#define REMOTEXY_SERIAL_SPEED 19200
#define REMOTEXY_WIFI_SSID "MasterHouse"
#define REMOTEXY_WIFI_PASSWORD "12345678"
#define REMOTEXY_SERVER_PORT 6377


#include <RemoteXY.h>

// RemoteXY GUI configuration  
#pragma pack(push, 1)  
uint8_t RemoteXY_CONF[] =   // 114 bytes
  { 255,4,0,0,0,107,0,19,0,0,0,77,97,115,116,101,114,72,111,117,
  115,101,0,31,1,106,200,1,1,5,0,10,7,40,24,24,48,4,26,31,
  79,78,0,31,79,70,70,0,10,40,40,24,24,48,4,26,31,79,78,0,
  31,79,70,70,0,10,74,41,24,24,48,4,26,31,79,78,0,31,79,70,
  70,0,10,41,78,24,24,48,4,26,31,79,78,0,31,79,70,70,0,129,
  30,15,43,12,0,8,67,117,97,114,116,111,115,0 };
  
// this structure defines all the variables and events of your control interface 
struct {

    // input variables
  uint8_t pushSwitch_01; // =1 if state is ON, else =0
  uint8_t pushSwitch_02; // =1 if state is ON, else =0
  uint8_t pushSwitch_03; // =1 if state is ON, else =0
  uint8_t pushSwitch_04; // =1 if state is ON, else =0

    // other variable
  uint8_t connect_flag;  // =1 if wire connected, else =0

} RemoteXY;   
#pragma pack(pop)
 
/////////////////////////////////////////////
//           END RemoteXY include          //
/////////////////////////////////////////////
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  RemoteXY_Init ();
  Serial.begin(9600);
  for (int i = 0; i <= 6; i++) {
    pinMode(luces[i], OUTPUT);
  }
  dht.begin();
  pinMode(pirPin, INPUT);
  Garage.attach(8);
  Garage.write(90);
}

void loop() {
  RemoteXY_Handler ();
  int val = digitalRead(pirPin); 
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  int shg = analogRead(PIN_MQ2);
  int sensorluz = analogRead(A0);
  if(RemoteXY.pushSwitch_01 ==1){
    digitalWrite(luces[0],HIGH);
    estadoluces[0] = 1;
    }else{
      digitalWrite(luces[0],LOW);
      estadoluces[0] = 0;
      }
     if(RemoteXY.pushSwitch_02 ==1){
    digitalWrite(luces[1],HIGH);
    estadoluces[1] = 1;
    }else{
      digitalWrite(luces[1],LOW);
      estadoluces[1] = 0;
      }
    if(RemoteXY.pushSwitch_03 ==1){
    digitalWrite(luces[2],HIGH);
    estadoluces[2] = 1;
    }else{
      digitalWrite(luces[2],LOW);
      estadoluces[2] = 0;
      }
    if(RemoteXY.pushSwitch_04 ==1){
    digitalWrite(luces[3],HIGH);
    estadoluces[3] = 1;
    }else{
      digitalWrite(luces[3],LOW);
      estadoluces[3] = 0;
      }
  
  if (Serial.available() > 1) {
    String Comando = Serial.readString();
    Comando.trim();
    if (Comando == "Cuarto1") {
      mleds(0, Comando);
    } else if (Comando == "Cuarto2") {
      mleds(1, Comando);
    } else if (Comando == "Cuarto3") {
      mleds(2, Comando);
    } else if (Comando == "Cuarto4") {
      mleds(3, Comando);
    } else if (Comando == "Patio") {
      mleds(4, Comando);
    } else if (Comando == "Entrada") {
      mleds(5, Comando);
    } else if (Comando == "ModoAutomatico") {
      modoAutomatico = (!modoAutomatico)? true: false;
    } else if (Comando == "Sala") {
      mleds(6, Comando);
    }else if (Comando == "Garage") {
      if(estado_garage){
        for (int pos = Garage.read(); pos <= 90; pos++) {
          Garage.write(pos);
          RemoteXY_delay(15);
        }
        estado_garage = false;
      }else{
        for (int pos = Garage.read(); pos >= 0; pos--) {
          Garage.write(pos);
          RemoteXY_delay(15);
        }
        estado_garage = true;
        }
    } else {
      Serial.println("Ese comando no existe");
    }
  }

  //Configuracion modo automatico
  if(modoAutomatico == true && sensorluz <=200){
    digitalWrite(luces[4], LOW);
    digitalWrite(luces[5], LOW);
    estadoluces[4] = 0;
    estadoluces[5] = 0;
    } else if(modoAutomatico == true && sensorluz >=200){
      digitalWrite(luces[4], HIGH);
      digitalWrite(luces[5], HIGH);
      estadoluces[4] = 1;
      estadoluces[5] = 1;
      }

  //Configuracion sensor de movimientos
  if (val == HIGH) {
    digitalWrite(luces[6], HIGH);  
    estadoluces[6] = 1;
    if (pirState == LOW) {
      pirState = HIGH;
    }
  } else {
    digitalWrite(luces[6], LOW); 
    estadoluces[6] = 0;
    if (pirState == HIGH) {
      pirState = LOW;
    }
  }

  //Imprimir datos para lectura del Programa
  Serial.print(t);
  Serial.print("/");
  Serial.print(h);
  Serial.print("/");
  for (int i = 0; i <= 6; i++) {
    Serial.print(estadoluces[i]);
  }
  Serial.print("/");
  Serial.print(sensorluz);
  Serial.print("/");
  Serial.print(shg);
  Serial.println("\n");
  RemoteXY_delay(1000);
}

void mleds(int led, String cuarto) {
  if (estadoluces[led] == 0) {
    digitalWrite(luces[led], HIGH);
    estadoluces[led] = 1;
    //Serial.println("Encendiendo " + cuarto);
  } else {
    digitalWrite(luces[led], LOW);
    estadoluces[led] = 0;
    //Serial.println("Apagando " + cuarto);
  }
}
