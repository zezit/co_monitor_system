// Bibliotecas utilizadas pelo MQTT
#include <WiFi.h>
#include <PubSubClient.h>
// Biblioteca utilizadas pela configuração via WIFI
#include <DNSServer.h>
#include <WiFiManager.h>
// Bibliotecas gerais
#include <EEPROM.h>

// ======================== DEFINES ========================

// Pinos utilizados pelo hardware
#define SENSOR_PIN 1
#define BUZZER_PIN  7

// Limite de CO que gera alarme
#define ALARM_VALUE 2.5 // Percentual

// Número de bytes utilizados na flash
#define EEPROM_SIZE 3

// ===================== VARIÁVEIS GLOBAIS =====================

// Nome e senha do wifi
const char* ssid = "Multilaser_2.4G_D35E40";
const char* password = "";

// Endereço do broker MQTT
const char* mqtt_server = "mqtt.eclipseprojects.io";

// Cria o objeto do client do WIFI
WiFiClient espClient;

// Cria o objeto do client do MQTT
PubSubClient client(espClient);

// Variáveis para contar o tempo
long lastMsg = 0;

// Flag de alarme
bool alarme = false;

// Flag que indica se está sem configuração
bool default_values = true;

// Leitura do sensor
int analog = 0; // Raw
float porcentagem = 0; // Porcentagem

// Variáveis de configuração via MQTT
bool sendAllReadings = false;
int sendingTimeoutSeconds = 1;

// Flag que indica a simulação de um alarme
bool fake_alarm = false;

// ======================== FUNÇÕES ========================

// Inicialização do programa
void setup() {
  // Inicializa a porta serial
  Serial.begin(115200);

// Configura a rede WIFI
  setup_config_wifi();

  // Inicializa a memória flash
  EEPROM.begin(EEPROM_SIZE);

  // Verifica se o equipamento já foi configurado
  default_values = EEPROM.read(0);

  // Atualiza as configurações
  if (default_values == false) {
    sendAllReadings = EEPROM.read(1);
    sendingTimeoutSeconds = EEPROM.read(2);
  }

  // Valores iniciais
  Serial.print(" \t \t - default_values: ");
  Serial.print(default_values);
  Serial.print("\n  \t \t - send_all_readings: ");
  Serial.print(sendAllReadings);
  Serial.print("\n \t \t - sending_timeout_seconds: ");
  Serial.println(sendingTimeoutSeconds);

  // Inicializa o WIFI
  setup_wifi();

  // Inicializa o MQTT
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  // Inicializa os pinos utilizados
  pinMode(SENSOR_PIN, INPUT); // Entrada
  pinMode(BUZZER_PIN, OUTPUT); // Saida
}

// Loop principal
void loop() {
  // --------------- CONEXÃO MQTT ---------------
  // Verifica se o server MQTT está conectado
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // --------------- LEITURA SENSOR ---------------
  // Lê o valor do sensor
  analog = analogRead(SENSOR_PIN);

  if (fake_alarm) {
    porcentagem = 5;
  } else {
    porcentagem = (float)analog / 1000;
  }

  // Verifica se está próximo de 250 ppm
  if (porcentagem >= ALARM_VALUE) {
    digitalWrite(BUZZER_PIN, HIGH);
    alarme = true;
  }
  else {
    digitalWrite(BUZZER_PIN, LOW);
    alarme = false;
  }

  // --------------- ENVIO DO PACOTE ---------------
  // Envia o valor a cada 3 segundos
  long now = millis();
  if (now - lastMsg > sendingTimeoutSeconds * 1000) {
    lastMsg = now;

    Serial.print("LEITURA: ");
    Serial.println(porcentagem);

    // Verifica se as mensagens devem ser sempre enviadas
    if (sendAllReadings == false) {
      // Verifica se o alarme foi acionado para enviar o valor
      if (alarme == false)
        return;
    }

    // Cria um objeto JSON com o valor lido
    String json = "{\"co_level\":" + String(porcentagem, 1) + ",\"analog_read\":" + String(analog) +  "}";

    Serial.print("CO Level: ");
    Serial.println(json);

    // Converte a String em char array
    char jsonBuffer[json.length() + 1];
    json.toCharArray(jsonBuffer, json.length() + 1);

    // Publica a mensagem
    client.publish("sensor/sub", jsonBuffer);

    delay(100);
  }
}
