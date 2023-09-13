import json
import time
import random
from mqtt_service import MQTTService
from config_manager import ConfigManager
from whatsapp_alert import WhatsAppAlert
import telegram_bot

from dotenv import load_dotenv
from flask import Flask, request, jsonify
import os

from ultrabot import ultraChatBot
from mqtt_service import MQTTService

load_dotenv()  # pega as variáveis de ambiente do arquivo .env

# enviorment

# mqtt configuration
MQTT_BROKER_URI = str(os.getenv('MQTT_BROKER'))
MQTT_PORT = int(os.getenv('MQTT_PORT'))
MQTT_SUBSCRIBE_TOPIC = str(os.getenv('MQTT_SUBSCRIBE_TOPIC'))
MQTT_PUBLISH_TOPIC = str(os.getenv('MQTT_PUBLISH_TOPIC'))
MQTT_CLIENT_ID = str(os.getenv('MQTT_CLIENT_ID'))
TELEGRAM_BOT_API_KEY = str(os.getenv('TELEGRAM_BOT_API_KEY'))
CALLMEBOT_API_KEY= str(os.getenv('CALLMEBOT_API_KEY'))
TELEFONE= str(os.getenv('TELEFONE'))

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
    warning_message = f"Nível alto de CO dectectado: {co_level}" if co_level > config_manager.get_threshold() else "Sem alarmes"
    return warning_message


def treat_sending():
    global co_level
    global passed_threshold
    global last_send_time

    packet_co_level = ""

    if (co_level != -500):
        packet_co_level = jsonify(co_level)
        # print(packet_co_level)

    # Caso estiver configurado para enviar apenas quando passar do threshold
    # Envia e reseta o valor do CO e a flag de enviado
    # Por padrão esse envio será de 10 em 10 segundos
    if (config_manager.get_send_only_threshold() and passed_threshold):
        print("\033[91m" + "ONLY THRESHOLD SEND" + "\033[0m")

        telegram_bot.send_reading(str(packet_co_level), config_manager, TELEFONE, CALLMEBOT_API_KEY)
        # TODO - remove debug
        print(json.dumps(packet_co_level, indent=4, sort_keys=True))
        print("")
        print("Next send will be in: ", time.asctime(
            time.localtime(time.time() + config_manager.get_sending_timeout_seconds())))
        co_level = -500
        passed_threshold = False
        # time.sleep(10)
        return

    # Caso configurado para enviar todas as leituras
    # Envia e reseta o valor do CO e a flag de enviado
    # Por padrão esse envio será de 10 em 10 segundos
    if (config_manager.get_send_all_readings()):
        print("\033[91m" + "SEND ALL READINGS" + "\033[0m")

        last_send_time = telegram_bot.send_reading(
            str(packet_co_level), config_manager, TELEFONE, CALLMEBOT_API_KEY)

        # TODO - remove debug
        print(json.dumps(packet_co_level, indent=4, sort_keys=True))
        print("")
        print("Next send will be in: ", time.asctime(
            time.localtime(time.time() + config_manager.get_sending_timeout_seconds())))
        co_level = -500
        passed_threshold = False
        return

    # Caso configurado para enviar leituras a cada X segundos
    # Envia e reseta o valor do CO e a flag de enviado
    # Por padrão esse envio será de 10 em 10 segundos
    elif (config_manager.check_sending_timeout(last_send_time) or passed_threshold):
        print("\033[91m" + "SENDING TIMEOUT" + "\033[0m")

        last_send_time = telegram_bot.send_reading(
            str(packet_co_level), config_manager, TELEFONE, CALLMEBOT_API_KEY)

        # TODO - remove debug
        print(json.dumps(packet_co_level, indent=4, sort_keys=True))
        print("")
        print("Next send will be in: ", time.asctime(
            time.localtime(time.time() + config_manager.get_sending_timeout_seconds())))

    co_level = -500
    passed_threshold = False


def on_message_callback(client, userdata, message):
    global co_level
    global passed_threshold

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
        if (not isinstance(reading_co_level, int)):
            print("Invalid JSON")
            return

        co_level = reading_co_level  # Atualiza o valor do co_level
        passed_threshold = config_manager.check_treshhold(
            co_level)  # Verifica se passou do threshold

        treat_sending()


def main():
    while True:
        # delay witout blocking the loop
        time.sleep(1)
        pass


if __name__ == "__main__":
    last_send_time = 0
    passed_threshold = False
    co_level = -500
    packet_co_level = ""

    # Initialize configuration manager
    config_manager = ConfigManager()

    # Initialize MQTT service
    mqtt_service = MQTTService(MQTT_BROKER_URI, on_message_callback)
    print("MQTT service initialized")
    # Initialize sub to ESP32
    mqtt_service.subscribe_to_topic(MQTT_SUBSCRIBE_TOPIC, on_message_callback)
    print("Subscribed to topic: ", MQTT_SUBSCRIBE_TOPIC)
    # Initialize Telegram bot
    telegram_bot.botInit(TELEGRAM_BOT_API_KEY, config_manager, mqtt_service)
    main()
    # configuration packet example (sensor/sub/config):
    # TODO
    """ 
    {
        "threshold": 100,
        "send_all_readings": false,
        "sending_timeout_seconds": 10
        "send_only_threshold": false
    }
    """


# https://mqtthq.com/client