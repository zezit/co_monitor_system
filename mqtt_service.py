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

    """ 
    {
        "threshold": 100,
        "send_all_readings": false,
        "sending_timeout_seconds": 10
        "send_only_threshold": false
    }
    """

    def config_send_time(self, time, actual_values):
        threshold, send_all_readings, _, send_only_threshold = actual_values

        json_packet = {
            "threshold": threshold,
            "send_all_readings": send_all_readings,
            "sending_timeout_seconds": time,
            "send_only_threshold": send_only_threshold
        }

        self.client.publish("sensor/config", str(json_packet))

    def config_threshold(self, threshold, actual_values):
        _, send_all_readings, send_only_threshold, sending_timeout_seconds = actual_values

        json_packet = {
            "threshold": threshold,
            "send_all_readings": send_all_readings,
            "sending_timeout_seconds": sending_timeout_seconds,
            "send_only_threshold": send_only_threshold
        }

        self.client.publish("sensor/config", str(json_packet))

    def config_send_all_readings(self, actual_values):
        threshold, _, sending_timeout_seconds, _ = actual_values
        json_packet = {
            "threshold": threshold,
            "send_all_readings": True,
            "sending_timeout_seconds": sending_timeout_seconds,
            "send_only_threshold": False
        }
        self.client.publish("sensor/config", str(json_packet))

    def config_send_only_threshold(self, actual_values):
        threshold, send_all_readings, _, _ = actual_values
        json_packet = {
            "threshold": threshold,
            "send_all_readings": False,
            "sending_timeout_seconds": 0,
            "send_only_threshold": True
        }
        self.client.publish("sensor/config", str(json_packet))
