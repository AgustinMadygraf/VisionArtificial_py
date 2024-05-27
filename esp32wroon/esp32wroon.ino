#include <WiFi.h>
#include <WebServer.h>

// Configura el SSID y la contraseña de tu red WiFi
const char* ssid = "Aula tecnica";
const char* password = "Madygraf32";

// Configura los pines de salida
const int pinOutput_ENA = 18; // enciende el motor con LOW
const int pinOutput_DIR = 19; // sentido de giro
const int pinOutput_PUL = 21; // pulso, debe tener 1000 microsegundos entre semiciclo positivo y negativo

WebServer server(80);

void handleRoot() {
  server.send(200, "text/plain", "ESP32 Web Server");
}

void handleOutputENA_f() {
  digitalWrite(pinOutput_ENA, LOW); // ENA se enciende con LOW
  server.send(200, "text/plain", "Motor en Marcha");
}

void handleOutputENA_r() {
  digitalWrite(pinOutput_ENA, HIGH); // ENA se apaga con HIGH
  server.send(200, "text/plain", "Motor Detenido");
}

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.println("WiFi connected");

  // Imprime la dirección IP obtenida
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  // Configura los pines de salida
  pinMode(pinOutput_ENA, OUTPUT);
  pinMode(pinOutput_DIR, OUTPUT);
  pinMode(pinOutput_PUL, OUTPUT);

  // Configura los pines en estado inicial
  digitalWrite(pinOutput_ENA, HIGH); // El motor está apagado inicialmente
  digitalWrite(pinOutput_DIR, LOW); // El sentido de giro es hacia adelante inicialmente
  digitalWrite(pinOutput_PUL, LOW); // El pulso está en estado bajo inicialmente

  server.on("/", handleRoot);
  server.on("/ena_f", handleOutputENA_f);
  server.on("/ena_r", handleOutputENA_r);

  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
}
