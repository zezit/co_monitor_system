import json
import time
import random
from mqtt_service import MQTTService
from config_manager import ConfigManager
# from whatsapp_alert import WhatsAppAlert
import telegram_bot

from dotenv import load_dotenv
# from flask import Flask, request, jsonify
import os

from mqtt_service import MQTTService

from database import Repository

load_dotenv()  # pega as variáveis de ambiente do arquivo .env

# enviorment

# mqtt configuration
MQTT_BROKER_URI = str(os.getenv('MQTT_BROKER'))
MQTT_PORT = int(os.getenv('MQTT_PORT'))
MQTT_SUBSCRIBE_TOPIC = str(os.getenv('MQTT_SUBSCRIBE_TOPIC'))
MQTT_PUBLISH_TOPIC = str(os.getenv('MQTT_PUBLISH_TOPIC'))
MQTT_CLIENT_ID = str(os.getenv('MQTT_CLIENT_ID'))
TELEGRAM_BOT_API_KEY = str(os.getenv('TELEGRAM_BOT_API_KEY'))
CALLMEBOT_API_KEY = str(os.getenv('CALLMEBOT_API_KEY'))
TELEFONE = str(os.getenv('TELEFONE'))

# WhatsApp numbers
from_whatsapp_number = "whatsapp:+1234567890"
to_whatsapp_number = "whatsapp:+9876543210"

config_manager = None
mqtt_service = None
last_send_time = None
passed_threshold = None
co_level = -500


def read_co_sensor():
    # Simulate CO sensor readings (replace with actual sensor reading logic)
    if (time.time() % 10 == 0):
        # Simulate sending every 10 seconds
        return random.randint(1, 200)
    else:
        return -500


def jsonify(co_level):
    return f"Nível de CO dectectado: {co_level}%"


def treat_sending():
    global co_level
    global passed_threshold
    global last_send_time

    packet_co_level = ""

    if (co_level != -500):
        packet_co_level = jsonify(co_level)

    last_send_time = telegram_bot.send_reading(
        str(packet_co_level), config_manager, config_manager.telefone, config_manager.wpp_api)

    # TODO - remove debug
    print(json.dumps(packet_co_level, indent=4, sort_keys=True))
    print("")

    co_level = -500


def on_message_callback(client, userdata, message):
    global co_level
    print("READING")

    # Reading packet (sensor/pub):
    """
    {
        "co_level": 100
    }
    """
    if (message.topic == MQTT_SUBSCRIBE_TOPIC):
        print("")
        print("Received reading packet:")
        try:
            print(json.dumps(json.loads(message.payload.decode()),
                             indent=4, sort_keys=True))
        except ValueError as e:
            print(message.payload.decode())
        print("")

        # Verifca se é um json válido
        try:
            json.loads(message.payload.decode())
        except ValueError as e:
            print("Invalid JSON")
            return

        # Verifica se o json possui o campo co_level
        if ("co_level" not in json.loads(message.payload.decode())):
            print("Invalid JSON")
            return

        reading_co_level = json.loads(message.payload.decode())["co_level"]

        # Verifica se o valor do co_level é um número
        if (not isinstance(reading_co_level, float)):
            print("Invalid JSON")
            return

        co_level = reading_co_level  # Atualiza o valor do co_level

        treat_sending()


def main():
    while True:
        pass


if __name__ == "__main__":
    last_send_time = 0
    co_level = -500
    packet_co_level = ""

    db = Repository(str(os.getenv('SUPABASE_URL')),
                    str(os.getenv('SUPABASE_KEY')))

    saved_config = db.get_saved_cred()

    # Initialize configuration manager
    config_manager = ConfigManager(saved_config)

    # Initialize MQTT service
    mqtt_service = MQTTService(MQTT_BROKER_URI, on_message_callback)
    print("MQTT service initialized")
    # Initialize sub to ESP32
    mqtt_service.subscribe_to_topic(MQTT_SUBSCRIBE_TOPIC, on_message_callback)
    print("Subscribed to topic: ", MQTT_SUBSCRIBE_TOPIC)

    # Initialize Telegram bot
    telegram_bot.botInit(TELEGRAM_BOT_API_KEY,
                         config_manager, mqtt_service, db)
    main()
# https://mqtthq.com/client
