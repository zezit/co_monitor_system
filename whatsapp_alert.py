# class WhatsAppAlert:
#     def __init__(self, account_sid, auth_token):
#         self.client = Client(account_sid, auth_token)

#     def send_alert(self, recipient_number, message):
#         try:
#             self.client.messages.create(
#                 body=message,
#                 from_='whatsapp:your_twilio_number',
#                 to=f'whatsapp:{recipient_number}'
#             )
#         except Exception as e:
#             print(f"Failed to send WhatsApp message: {str(e)}")
