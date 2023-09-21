# Código do Firmware

Este documento fornece instruções sobre como utilizar o código do firmware do sistema de monitoramento de Monóxido de Carbono (CO) nos arquivos `CO_monitor.ino` e `funcoes.ino`. Este código é projetado para rodar em um dispositivo ESP32S2 e integra-se com MQTT para comunicação de dados.

## Pré-requisitos

Antes de começar, assegure-se de ter os seguintes pré-requisitos:

- Placa ESP32S2 (ou similar)
- Ambiente de desenvolvimento Arduino IDE configurado para ESP32S2
- Biblioteca WiFiManager instalada na Arduino IDE (pode ser instalada via Gerenciador de Bibliotecas da Arduino IDE)
- Biblioteca PubSubClient instalada na Arduino IDE (pode ser instalada via Gerenciador de Bibliotecas da Arduino IDE)

## Configuração

1. Abra o arquivo `CO_monitor.ino` na Arduino IDE.

2. Certifique-se de que a placa ESP32S2 está selecionada nas configurações da Arduino IDE (Ferramentas -> Placa).

3. Configure o nome e a senha da rede Wi-Fi nas variáveis `ssid` e `password`:

   ```cpp
   const char* ssid = "NomeDaSuaRede";
   const char* password = "SuaSenhaDeRede";
   ```

4. Configure o endereço do broker MQTT nas variáveis `mqtt_server`:

   ```cpp
   const char* mqtt_server = "mqtt.eclipseprojects.io";
   ```

5. Defina os pinos utilizados pelo hardware nas variáveis `SENSOR_PIN` e `BUZZER_PIN` de acordo com a conexão dos sensores:

   ```cpp
   #define SENSOR_PIN 1
   #define BUZZER_PIN  7
   ```

6. Configure o limite de CO que gera um alarme na variável `ALARM_VALUE`. Por padrão, está definido como 2.5%:

   ```cpp
   #define ALARM_VALUE 2.5 // Percentual
   ```

7. Compile o código e faça o upload para o seu dispositivo ESP32S2.

## Uso

Após carregar o código no dispositivo ESP32S2, ele funcionará como um monitor de CO e enviará leituras para um servidor MQTT.

- O dispositivo tentará se conectar à sua rede Wi-Fi configurada durante a inicialização.

- Uma vez conectado à rede Wi-Fi, ele tentará se conectar ao servidor MQTT configurado.

- O dispositivo realizará leituras do sensor de CO e enviará os dados para o servidor MQTT.

- Se o valor de CO exceder o limite definido em `ALARM_VALUE`, o dispositivo ativará um alarme no pino `BUZZER_PIN`.

## Notas Adicionais

- O código inclui funcionalidade de configuração inicial via Wi-Fi. Quando o dispositivo é ligado pela primeira vez, ele cria um Access Point (AP) chamado "CO_MONITOR" com a senha "12345678" para que você possa configurar o Wi-Fi.

- O código utiliza a biblioteca WiFiManager para facilitar a configuração do Wi-Fi.

- O código também suporta configuração de parâmetros adicionais (como o tempo de envio de dados) via MQTT. Você pode configurar esses parâmetros enviando mensagens para o tópico "sensor/config" no servidor MQTT.

- O dispositivo fará leituras periódicas do sensor e enviará os dados para o tópico "sensor/sub" no servidor MQTT.

- Certifique-se de ter a placa ESP32S2 devidamente configurada na Arduino IDE e as bibliotecas PubSubClient e WiFiManager instaladas para compilar e carregar o código no dispositivo.