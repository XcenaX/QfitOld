import random
import string
import datetime

from twilio.rest import Client 
from qfit.settings import TWILIO_CODE

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def get_random_string_of_numbers(length):
    letters = ["0","1","2","3","4","5","6","7","8","9"]
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def check_image_type(image):
    try:
        if not image.name.endswith(".png") and not image.name.endswith(".jpg"):
            return False
    except:
        return False
    return True

def check_timelines(schedules):
    for schedule in schedules:
        for another_timeline in schedule["timelines"]:
            for timeline in schedule["timelines"]:
                if timeline["id"] != another_timeline["id"]:
                    another_start_time = datetime.datetime.strptime(another_timeline["start_time"], "%H:%M")
                    another_end_time = datetime.datetime.strptime(another_timeline["end_time"], "%H:%M")
                    start_time = datetime.datetime.strptime(timeline["start_time"], "%H:%M")
                    end_time = datetime.datetime.strptime(timeline["end_time"], "%H:%M")
                    if another_start_time < start_time and another_end_time > start_time or another_start_time < end_time and another_end_time > end_time or another_end_time == end_time or another_start_time == start_time or another_end_time <= another_start_time or end_time <= start_time or another_start_time > start_time and another_end_time < end_time:
                        return False
    return True

def send_sms(to, message):
    account_sid = 'AC7727dd61dab28c7a073c7702515da0e8' 
    auth_token = TWILIO_CODE
    client = Client(account_sid, auth_token) 
    
    message = client.messages.create(  
        messaging_service_sid='MG6ab91f013109df58bc4811e674231c85', 
        body=message,      
        to=to
    ) 
