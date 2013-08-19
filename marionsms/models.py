# -*- coding: utf-8 -*-
from .extensions import db



class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, db.Sequence('questions_id_seq'), primary_key=True)
    name = db.Column(db.String(255))
    text = db.Column(db.Text)

    scheduled_questions = db.relationship('ScheduledQuestion', backref='question')

    def __init__(self, name=None, text=None):
        self.name = name
        self.text = text

    def __repr__(self):
        return "<Question({})::{}>".format(self.id, self.text)


class ScheduledQuestion(db.Model):
    __tablename__ = 'scheduled_questions'
    id = db.Column(db.Integer, db.Sequence('scheduled_questions_id_seq'), primary_key=True)
    phone_number = db.Column('phone_number', db.String(255))
    question_id = db.Column('question_id', db.Integer, db.ForeignKey('questions.id'))
    time = db.Column('time', db.String(512))
    
    def __init__(self, phone_number=None, question_id=None, time=None):
        self.phone_number = phone_number
        self.question_id = question_id
        self.time = time

    def __repr__(self):
        return "<ScheduledQuestion({}::{}::{})>".format(self.phone_number, self.time, self.question.name)

