/*
   Arquivo com as funções utilizadas
*/

// ==================== INICIALIZAÇÕES =====================

// Configura o WIFI para receber dados
void setup_config_wifi() {
  WiFiManager wifiManager;
  wifiManager. setConfigPortalTimeout(240);

  // Cria uma Access Point com o nome da rede e a senha
  if (!wifiManager.autoConnect("CO_MONITOR", "12345678")) {
    Serial.println(F("Connection failed. Reset and try again..."));
    delay(3000);
    ESP.restart();
    delay(5000);
  }

  //Message if connection OK
  Serial.println(F( "Connected to the Wifi network."));
  Serial.print(F("IP Address: "));
  Serial.println(WiFi.localIP());
}

// Inicialização do WIFI
void setup_wifi() {
  delay(10);

  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  // Tenta conectar com o WIFI
  WiFi.begin(ssid, password);

  // Aguarda até conectar com sucesso
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

// ==================== CALLBACKS =====================

// Função de callback de mensagens do MQTT
void callback(char* topic, byte* message, unsigned int length) {
  Serial.println("===========================");
  Serial.print("\n \t - Mensagem recebida no tópico:    ");
  Serial.print(topic);
  Serial.print(". \n \t - Mensagem: ");
  String messageTemp;

  // Printa a mensagem recebida
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();

  // Converte a String em char array
  char msgBuffer[messageTemp.length() + 1];
  messageTemp.toCharArray(msgBuffer, messageTemp.length() + 1);

  // Verifica se a mensagem recebida é do tópico esperado
  if (String(topic) == "sensor/config") {
    // Encontra a posição das palavras no pacote recebido
    char *trueStr = strstr(msgBuffer, "True");
    char *falseStr = strstr(msgBuffer, "False");
    char *alarmStr = strstr(msgBuffer, "Alarm");

    fake_alarm = false;

    if (trueStr != NULL) {
      sendAllReadings = true;
    } else if (falseStr != NULL) {
      sendAllReadings = false;
    } else if (alarmStr != NULL) {
      fake_alarm = true;
    }

    // Pega o valor do tempo de envio no pacote
    char *token = strtok(msgBuffer, ":,");
    while (token != NULL) {
      if (strstr(token, "sending_timeout_seconds") != NULL) {
        token = strtok(NULL, ":,");
        sendingTimeoutSeconds = atoi(token);
        break;
      }
      token = strtok(NULL, ":,");
    }

    // Limita o valor do tempo de envio
    if (sendingTimeoutSeconds == 0)
      sendingTimeoutSeconds = 1;
    else if (sendingTimeoutSeconds >= 255)
      sendingTimeoutSeconds = 255;

    default_values = false; // Indica que recebeu configuração

    EEPROM.write(0, default_values);
    EEPROM.write(1, sendAllReadings);
    EEPROM.write(2, sendingTimeoutSeconds);
    EEPROM.commit();

    Serial.print(" \t \t - send_all_readings: ");
    Serial.print(sendAllReadings);
    Serial.print("\n \t \t - sending_timeout_seconds: ");
    Serial.print(sendingTimeoutSeconds);


    Serial.println("===========================");
    Serial.println();
  }
}

// Função de reconexão com o server MQTT
void reconnect() {
  // Aguarda até conectar com sucesso
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");

    // Tenta conectar
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");
      // Subscribe
      client.subscribe("sensor/config");
    }
    else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 1 seconds");

      // Aguarda 3 segundos antes de tentar conectar novamente
      delay(1000);
    }

    // Aciona o buzzer para indicar que não está conectado
    digitalWrite(BUZZER_PIN, HIGH);
    delay(500);
    digitalWrite(BUZZER_PIN, LOW);
    delay(500);
  }
}

