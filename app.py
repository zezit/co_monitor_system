# License: MIT License
import json
import time
import random
import os
import telegram_bot
from dotenv import load_dotenv

# Local imports
from mqtt_service import MQTTService
from config_manager import ConfigManager
from localdb import LocalRepository

load_dotenv()  # pega as variáveis de ambiente do arquivo .env

# enviorment

# mqtt configuration
MQTT_BROKER_URI = str(os.getenv('MQTT_BROKER'))
MQTT_PORT = int(os.getenv('MQTT_PORT'))
MQTT_SUBSCRIBE_TOPIC = str(os.getenv('MQTT_SUBSCRIBE_TOPIC'))
MQTT_PUBLISH_TOPIC = str(os.getenv('MQTT_PUBLISH_TOPIC'))
TELEGRAM_BOT_API_KEY = str(os.getenv('TELEGRAM_BOT_API_KEY'))

config_manager = None
mqtt_service = None


def treat_sending():
    global co_level

    packet_co_level = f"Nível de CO dectectado: {co_level}%"

    print("")
    print(json.dumps(packet_co_level, indent=4, sort_keys=True))
    print("")
    
    telegram_bot.send_reading(packet_co_level, config_manager)


def on_message_callback(client, userdata, message):
    global co_level

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
            print("Invalid JSON - Não possui o campo co_level")
            return

        reading_co_level = json.loads(message.payload.decode())["co_level"]

        # Verifica se o valor do co_level é um número
        if (not isinstance(reading_co_level, float)):
            print("Invalid JSON - co_level não é um número float")
            return

        co_level = reading_co_level  # Atualiza o valor do co_level

        treat_sending()


def main():
    while True:
        pass


if __name__ == "__main__":
    db = LocalRepository("localdb.json")

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
