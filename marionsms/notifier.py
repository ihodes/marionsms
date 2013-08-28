# -*- coding: utf-8 -*-

from flask import current_app

import os
import datetime
from time import sleep
import twilio as tw
import twilio.rest as tr
import pytz
import string

from .extensions import db
from .models import ScheduledMessage


TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER')


def to_utc(timestamp):
    return datetime.datetime(year=timestamp.year,
                             month=timestamp.month,
                             day=timestamp.day,
                             hour=timestamp.hour,
                             minute=timestamp.minute,
                             tzinfo=pytz.timezone('UTC'))


def send_message(scheduled_message, client=None):
    if client is None:
        client = tr.TwilioRestClient()
    client.sms.messages.create(to=scheduled_message.phone_number,
                               from_=TWILIO_NUMBER,
                               body=scheduled_message.message.text)


def mark_last_sent(scheduled_message):
    scheduled_message.last_sent = datetime.datetime.now()
    db.session.add(scheduled_message)
    db.session.commit()
    

def send_nows_smss():
    now = to_utc(datetime.datetime.now())
    now_hour = datetime.time(hour=now.hour)
    scheduled_messages = ScheduledMessage.query.filter_by(time=now_hour, active=True).all()
    scheduled_messages = [sm for sm in scheduled_messages if not sm.message.hidden]

    client = tr.TwilioRestClient()

    for message in scheduled_messages:
        print "message: {}".format(message.message_id)
        if message.daily or message.day_of_week == string.lower(now.strftime('%A')):
            current_app.logger.info("Sending message {} at {}".format(message, now))
            send_message(message, client=client)
            mark_last_sent(message)
            sleep(1) # TK TODO hack hacky rate-limiting
            
