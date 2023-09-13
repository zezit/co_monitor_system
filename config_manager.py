import time


class ConfigManager:
    def __init__(self):
        self.threshold = 8 # 8%
        self.send_all_readings = False  # Funciona juntamente com o timeout
        self.sending_timeout_seconds = 15
        self.send_only_threshold = True  # Soprepoe o send_all_readings e o timeout
        self.serie_number = "8UPBcvyG"
        self.chat_id = None
        self.name = "Sensor de CO"

    def set_threshold(self, value):
        self.threshold = value
        return self.get_config()

    def set_send_all_readings(self, value):
        if (value):
            self.send_only_threshold = False
        self.send_all_readings = value
        return self.get_config()

    def get_threshold(self):
        return self.threshold

    def set_sending_timeout_seconds(self, value):
        self.sending_timeout_seconds = value
        return self.get_config()

    def set_send_only_threshold(self, value):
        if (value):
            self.send_all_readings = False
            self.sending_timeout_seconds = 0
        self.send_only_threshold = value

        return self.get_config()

    def get_send_all_readings(self):
        return self.send_all_readings

    def check_sending_timeout(self, last):
        if last is None:
            return True  # Treat this as the first message to send
        current_time = time.time()
        return (current_time - last) > self.sending_timeout_seconds

    def get_sending_timeout_seconds(self):
        return self.sending_timeout_seconds

    def get_send_only_threshold(self):
        return self.send_only_threshold

    def check_treshhold(self, value):
        return value > self.threshold

    def get_config(self):
        return self.threshold, self.send_all_readings, self.sending_timeout_seconds, self.send_only_threshold
