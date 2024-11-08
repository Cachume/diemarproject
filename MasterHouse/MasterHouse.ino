#include <DHT.h>
#include <DHT_U.h>

int luces[] = {13, 12, 11, 10, 7, 6};
int estadoluces[] = {0, 0, 0, 0, 0, 0};
bool modoAutomatico = false;

#define DHTPIN 2      // Pin al que está conectado el sensor
#define DHTTYPE DHT22 // Tipo de sensor DHT11

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
    } else if (Comando == "Garage") {
      mleds(4, Comando);
    } else if (Comando == "Entrada") {
      mleds(5, Comando);
    } else if (Comando == "ModoAutomatico") {
      modoAutomatico = true;
      while(modoAutomatico){
        int valor = analogRead(A2);
        Serial.println(valor);
        if((Serial.available() > 1)){
          modoAutomatico = false;
          } else if (valor <= 100){
            for (int i = 0; i <= 5; i++) {
              digitalWrite(luces[i], LOW);
            }
          } else if (valor > 35){
            for (int i = 0; i <= 5; i++) {
              digitalWrite(luces[i], HIGH);
            }
          }
        }
    } else {
      Serial.println("Ese comando no existe");
    }
  }
  Serial.print(h);
  Serial.print("/");
  Serial.print(t);
  Serial.print("/");
  for (int i = 0; i <= 3; i++) {
    Serial.print(estadoluces[i]);
  }
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
