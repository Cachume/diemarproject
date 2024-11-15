#include <DHT.h>
#include <DHT_U.h>

int luces[] = {13, 12, 11, 10, 7, 6};
int estadoluces[] = {0, 0, 0, 0, 0, 0};
bool modoAutomatico = false;

#define DHTPIN 2      // Pin al que está conectado el sensor
#define DHTTYPE DHT22 // Tipo de sensor DHT11
#define PIN_MQ2 A1 //Pin al que esta conectado el sensor de humo y gas

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  for (int i = 0; i <= 5; i++) {
    pinMode(luces[i], OUTPUT);
  }
  dht.begin();
}

void loop() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  int shg = analogRead(PIN_MQ2);
  int sensorluz = analogRead(A0);
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
    } else {
      Serial.println("Ese comando no existe");
    }
  }

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

  //Imprimir datos para lectura del Programa
  Serial.print(h);
  Serial.print("/");
  Serial.print(t);
  Serial.print("/");
  for (int i = 0; i <= 5; i++) {
    Serial.print(estadoluces[i]);
  }
  Serial.print("/");
  Serial.print(sensorluz);
  Serial.print("/");
  Serial.print(shg);
  Serial.println("\n");
  delay(1000);
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
