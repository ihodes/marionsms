# -*- coding: utf-8 -*-
import string
import datetime

from flask.ext.login import UserMixin

from .extensions import db, lm, bcrypt


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, db.Sequence('message_id_seq'), primary_key=True)
    name = db.Column('name', db.String(255))
    text = db.Column('text', db.String(160))

    scheduled_messages = db.relationship('ScheduledMessage', backref='message')
    responses = db.relationship('Response', backref='message')

    expect_response = db.Column('expect_response', db.Boolean, default=True)

    hidden = db.Column('hidden', db.Boolean, default=False)

    def __init__(self, name=None, text=None):
        self.name = name
        self.text = text

    def __repr__(self):
        return "Message({}, {})".format(self.name, self.text)


class ScheduledMessage(db.Model):
    __tablename__ = 'scheduled_messages'
    id = db.Column(db.Integer, db.Sequence('scheduled_message_id_seq'), primary_key=True)
    phone_number = db.Column('phone_number', db.String(255))
    message_id = db.Column('message_id', db.Integer, db.ForeignKey('messages.id'))

    time = db.Column('time', db.Time)

    # true if sent every day
    daily = db.Column('daily', db.Boolean)

    # only set if sent on e.g. Fridays
    day_of_week = db.Column('day_of_week', db.String(512))

    last_sent = db.Column('last_sent', db.DateTime)

    # True if the message should still be sent out, False if it's been canceled.
    active = db.Column('active', db.Boolean, default=True)

    def __init__(self, phone_number, message_id, time, frequency):
        self.phone_number = phone_number
        self.message_id = message_id
        self.time = time
        
        if frequency == 'daily':
            self.daily = True
        else:
            self.day_of_week = string.lower(frequency)

    @property
    def frequency(self):
        if self.daily:
            return 'daily'
        else:
            return self.day_of_week


    def __repr__(self):
        return "ScheduledMessage({}, {}, {}, {})".format(self.phone_number,
                                                         self.message_id,
                                                         self.time,
                                                         self.frequency)

    @property
    def time_as_localized_string(self):
        # should handle TZ issues... DST? TK TODO
        return str(self.time)

    @property
    def schedule_as_string(self):
        if self.daily:
            return "Daily at " + self.time_as_localized_string
        else:
            return (string.capitalize(self.day_of_week) + 
                    " at " + self.time_as_localized_string)


class Response(db.Model):
    __tablename__ = 'responses'
    id = db.Column(db.Integer, db.Sequence('response_id_seq'), primary_key=True)

    phone_number = db.Column('phone_number', db.String(255))
    answered_at = db.Column('answered_at', db.DateTime, default=datetime.datetime.now)
    text = db.Column('name', db.String(160))
    message_id = db.Column('message_id', db.Integer, db.ForeignKey('messages.id'))
    scheduled_message_id = db.Column('scheduled_message_id', db.Integer, db.ForeignKey('scheduled_messages.id'))

    def __init__(self, phone_number, text, message_id, scheduled_message_id):
        self.phone_number = phone_number
        self.text = text
        self.message_id = message_id
        self.scheduled_message_id = scheduled_message_id

    def __repr__(self):
        return "Response({}, {})".format(self.phone_number, self.text, self.answered_at)



class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)

    username = db.Column('username', db.Text)
    password = db.Column('password', db.Text)

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.generate_password_hash(password)

    def verify_password(self, password_candidate):
        return bcrypt.check_password_hash(self.password, password_candidate)

    def __repr__(self):
        return "User({})".format(self.username)
