import re
import string
from flask import json


from .extensions import db
from .models import Message, ScheduledMessage



def schedule(phone_number, message_id, frequency, time):
    sm = ScheduledMessage(phone_number, message_id, time, frequency)
    db.session.add(sm)
    db.session.commit()
    return sm


# TK TODO
def _schedule_process_csv(csv):
    with open(csv) as schedule:
        for line in schedule:
            parts = map(string.strip, line.split(','))
            assert(len(parts) == 3)

            phone_number = re.sub('\+|\(|\)|-| ', '', parts[0])
            assert(re.match('^\d{10,10}$', phone_number))

            messages = re.sub(' ', '', parts[1]).split('|')
            assert(all([re.match('\d+', q) for q in messages]))

            times = parts[2].split('|')
            assert(len(messages) == len(times))

            # schedule_messages(phone_number, messages, times)    
    
