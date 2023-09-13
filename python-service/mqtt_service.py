import time
import paho.mqtt.client as mqtt


class MQTTService:
    def __init__(self, broker_uri, callback=None):
        self.client = mqtt.Client("TESTE1")
        self.client.on_message = callback
        self.client.connect(broker_uri)
        self.client.loop_start()

    def publish_message(self, topic, message):
        self.client.publish(topic, message)
        return time.time()

    def subscribe_to_topic(self, topic, callback):
        self.client.subscribe(topic)
        self.client.on_message = callback

    def config_send_time(self, time, actual_values):
        _, send_all_readings, _ = actual_values
        print("send_all_readings: ", send_all_readings)

        json_packet = {
            "send_all_readings": send_all_readings,
            "sending_timeout_seconds": time,
        }

        print("json_packet: ", json_packet)

        self.client.publish("sensor/config", str(json_packet))

    def config_send_all_readings(self, actual_values):
        _, _, sending_timeout_seconds = actual_values
        json_packet = {
            "send_all_readings": True,
            "sending_timeout_seconds": sending_timeout_seconds,
        }
        self.client.publish("sensor/config", str(json_packet))

    def config_send_only_threshold(self):
        json_packet = {
            "send_all_readings": False,
            "sending_timeout_seconds": 0,
        }
        self.client.publish("sensor/config", str(json_packet))

    def config_name(self, name):
        json_packet = {
            "name": name
        }
        self.client.publish("sensor/config", str(json_packet))

    def simulate(self, config):
        _, _, sending_timeout_seconds = config
        json_packet = {
            "send_all_readings": "Alarm",
            "sending_timeout_seconds": sending_timeout_seconds,
        }
        print("Sending: ", json_packet)
        self.client.publish("sensor/config", str(json_packet))
