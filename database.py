
import os
from supabase import create_client, Client


class Repository:
    def __init__(self, url: str, key: str):
        self.url = url
        self.key = key
        self.supabase: Client = create_client(self.url, self.key)

    def get_saved_cred(self):
        response = self.supabase.table('credentials').select("*").execute()
        if len(response.data) == 0:
            return None, None, None

        else:
            try:
                telefone = response.data[0]['telefone']
            except:
                telefone = None

            try:
                wpp_api = response.data[0]['api']
            except:
                wpp_api = None

            try:
                chat_id = response.data[0]['chat_id']
            except:
                chat_id = None

            print("telefone: ", telefone)
            print("wpp_api: ", wpp_api)
            print("chat_id: ", chat_id)

            return telefone, wpp_api, chat_id

    def update_telefone(self, tel):
        response = self.supabase.table('credentials').select("*").execute()
        if len(response.data) == 0:
            # If no rows exist, insert a new row
            self.supabase.table('credentials').update(
                {'telefone': tel}).eq('id', 1).execute()
        else:
            # If rows exist, update the existing row(s) or specify a condition to update a specific row
            self.supabase.table('credentials').update(
                {'telefone': tel}).eq('id', 1).execute()

    def update_chat_id(self, chat_id):
        response = self.supabase.table('credentials').select("*").execute()
        if len(response.data) == 0:
            # If no rows exist, insert a new row
            self.supabase.table('credentials').update(
                {'chat_id': chat_id}).eq('id', 1).execute()
        else:
            # If rows exist, update the existing row(s) or specify a condition to update a specific row
            self.supabase.table('credentials').update(
                {'chat_id': chat_id}).eq('id', 1).execute()

    def update_api_key(self, api_key):
        response = self.supabase.table('credentials').select("*").execute()
        if len(response.data) == 0:
            # If no rows exist, insert a new row
            self.supabase.table('credentials').update(
                {'api': api_key}).eq('id', 1).execute()
        else:
            # If rows exist, update the existing row(s) or specify a condition to update a specific row
            self.supabase.table('credentials').update(
                {'api': api_key}).eq('id', 1).execute()

    def delete_telefone(self, tel):
        # Specify the condition to find the record with the given telefone
        condition = self.supabase.table(
            'credentials').delete().eq('telefone', tel)

        # Execute the delete operation
        response = condition.execute()

        # Check the response to see if the deletion was successful
        if response.error:
            print(
                f"Error deleting record with telefone {tel}: {response.error}")
        else:
            print(f"Record with telefone {tel} deleted successfully")

    def delete_chat_id(self, chat_id):
        # Specify the condition to find the record with the given telefone
        condition = self.supabase.table(
            'credentials').delete().eq('chat_id', chat_id)

        # Execute the delete operation
        response = condition.execute()

        # Check the response to see if the deletion was successful
        if response.error:
            print(
                f"Error deleting record with chat_id {chat_id}: {response.error}")
        else:
            print(f"Record with chat_id {chat_id} deleted successfully")

    def delete_api_key(self, api_key):
        # Specify the condition to find the record with the given telefone
        condition = self.supabase.table(
            'credentials').delete().eq('api', api_key)

        # Execute the delete operation
        response = condition.execute()

        # Check the response to see if the deletion was successful
        if response.error:
            print(
                f"Error deleting record with api_key {api_key}: {response.error}")
        else:
            print(f"Record with api_key {api_key} deleted successfully")
