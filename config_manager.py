import time


class ConfigManager:
    def __init__(self):
        self.send_all_readings = True  # Funciona juntamente com o timeout
        self.sending_timeout_seconds = 60
        self.serie_number = "8UPBcvyG"
        self.telefone = None
        self.wpp_api = None
        self.chat_id = None
        self.name = "Sensor de CO"

    def set_send_all_readings(self):
        self.send_all_readings = True
        return self.get_config()

    def set_sending_timeout_seconds(self, value):
        self.sending_timeout_seconds = value
        return self.get_config()

    def set_send_only_threshold(self, value):
        if (value):
            self.send_all_readings = False
            self.sending_timeout_seconds = 0

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
        return not self.send_all_readings

    def get_config(self):
        return "", self.send_all_readings, self.sending_timeout_seconds
