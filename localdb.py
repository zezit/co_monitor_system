import os
import json


class LocalRepository:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as file:
                    return json.load(file)
            except (json.JSONDecodeError, FileNotFoundError):
                print(f"Error loading data from {self.file_path}. Creating a new file.")
                # Create a new file with default data
                self.create_default_file()
                return {'telefone': None, 'api': None, 'chat_id': None, 'wpp_send': False}
        else:
            # Create file if it doesn't exist
            self.create_default_file()
            return {'telefone': None, 'api': None, 'chat_id': None, 'wpp_send': False}

    def create_default_file(self):
        with open(self.file_path, 'w') as file:
            json.dump({'telefone': None, 'api': None, 'chat_id': None, 'wpp_send': False}, file)

    def save_data(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.data, file)

    def get_saved_cred(self):
        return (
            self.data['telefone'],
            self.data['api'],
            self.data['chat_id'],
            self.data['wpp_send']
        )

    def update_telefone(self, tel):
        self.data['telefone'] = tel
        self.save_data()

    def update_chat_id(self, chat_id):
        self.data['chat_id'] = chat_id
        self.save_data()

    def update_api_key(self, api_key):
        self.data['api'] = api_key
        self.save_data()

    def update_send(self, wpp_send):
        self.data['wpp_send'] = wpp_send
        self.save_data()

    def delete_telefone(self):
        self.data['telefone'] = None
        self.save_data()

    def delete_chat_id(self):
        self.data['chat_id'] = None
        self.save_data()

    def delete_api_key(self):
        self.data['api'] = None
        self.save_data()
