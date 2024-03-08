from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()


account_sid = os.getenv('SID')
auth_token = os.getenv('AUTH_TOKEN')
client = Client(account_sid, auth_token)

def sendAlert(accident_start_time, accident_end_time):

    message = client.messages.create(
    from_='+91xxxxxxxxxx',
    body=f''' Emergency Alert!!!
            Accident Detected!
            from {accident_start_time:.2f} to {accident_end_time:.2f}''',
    to='+91yyyyyyyyyy'
    )
    print("Alert sended!")