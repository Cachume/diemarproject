int luces[] = {13, 12, 11, 10, 7, 6};
int estadoluces[] = {0, 0, 0, 0, 0, 0};
int lucesEncendidas = false;
void setup() {
  Serial.begin(9600);
  for (int i = 0; i <= 5; i++) {
    pinMode(luces[i], OUTPUT);
  }
}

void loop() {
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
    } else {
      Serial.println("Ese comando no existe");
    }
  }
}

void mleds(int led, String cuarto) {
  if (estadoluces[led] == 0) {
    digitalWrite(luces[led], HIGH);
    estadoluces[led] = 1;
    Serial.println("Encendiendo " + cuarto);
  } else {
    digitalWrite(luces[led], LOW);
    estadoluces[led] = 0;
    Serial.println("Apagando " + cuarto);
  }
}
