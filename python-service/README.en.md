# README for Using the Python Code

This README provides instructions on how to use the provided Python code (`app.py`) and associated modules for a Carbon Monoxide (CO) monitoring system. This code integrates with MQTT for data communication, a local database for storing configuration, and Telegram/WhatsApp for sending notifications. 

## Prerequisites

Before you begin, ensure you have the following prerequisites installed on your system:

- Python 3.10.6
- Paho-MQTT library (`paho-mqtt`)
- Python `dotenv` library
- `requests` library
- `pyTelegramBotAPI` library
- MQTT broker (e.g., Mosquitto)
- A Telegram Bot API key
- Access to WhatsApp API (optional, for WhatsApp notifications)

## Getting Started

1. Clone or download the code repository to your local machine.

2. Create a `.env` file in the same directory as `app.py` and define the following environment variables:

   - `MQTT_BROKER`: The MQTT broker's URI.
   - `MQTT_PORT`: The MQTT broker's port.
   - `MQTT_SUBSCRIBE_TOPIC`: The MQTT topic to subscribe to for CO level readings.
   - `MQTT_PUBLISH_TOPIC`: The MQTT topic to publish configuration updates.
   - `TELEGRAM_BOT_API_KEY`: Your Telegram Bot API key.

   Example `.env` file:

   ```
   MQTT_BROKER=mqtt://localhost
   MQTT_PORT=1883
   MQTT_SUBSCRIBE_TOPIC=sensor/co_level
   MQTT_PUBLISH_TOPIC=sensor/config
   TELEGRAM_BOT_API_KEY=your_telegram_bot_api_key
   ```

3. Install the required Python libraries using pip:

   ```shell
   pip install -r requirements.txt
   ```

4. Run the `app.py` script:

   ```
   python app.py
   ```

## Usage

Once the code is running, you can interact with the CO monitoring system via Telegram. Here are some available commands:

- **/start**: Start the bot and display the initial menu.

- **Configurar**: Access the configuration menu.

- **Simular Alarme**: Start or stop simulating CO alarms.

- **Voltar ao Menu Principal**: Return to the main menu.

- **Configurar Tempo**: Set the interval for sending CO readings (in seconds).

- **Configurar Modo**: Set the operation mode (send all readings or send only when the threshold is exceeded).

- **Apenas quando ultrapassar o limite**: Set the mode to send data only when the CO level exceeds a threshold.

- **Todas as leituras**: Set the mode to send all CO readings.

- **Ler configurações**: Display the current configuration settings.

- **Hab/Des Bot Telegram**: Enable or disable Telegram notifications.

- **Hab/Des Whatsapp**: Enable or disable WhatsApp notifications (requires WhatsApp API configuration).

- **Configurar Whatsapp**: Configure WhatsApp notifications (requires WhatsApp API and phone number).

## Additional Notes

- The code also includes an optional feature for sending WhatsApp notifications. To enable this feature, you need to set up a WhatsApp API and provide the API key and phone number in the configuration.

- The code includes error handling, so if there are any issues with configuration or communication, error messages will be displayed.

- You can modify the code to adapt it to your specific requirements or integrate additional features as needed.

- The local database (`localdb.json`) stores configuration data. It is automatically created if it doesn't exist.

- The MQTT topics and payload formats can be customized as needed for your specific use case.

- The code provides flexibility in configuring the mode of operation and sending interval to suit different monitoring scenarios.