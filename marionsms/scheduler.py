import re
import string
from flask import json


from .extensions import db
from .models import Question, ScheduledQuestion


# parse and insert admissable lines in DB
#  inadmissable lines should be reported somehow (and correctable)
#  (asserts should be replaced with reporting)


def schedule(data, fmt=None):
    if fmt == 'csv':
        _schedule_process_csv(data)
    elif fmt == 'json':
        _schedule_process_json(data)
    else:
        _schedule_process(data)


def _schedule_process_csv(csv):
    with open(csv) as schedule:
        for line in schedule:
            parts = map(string.strip, line.split(','))
            assert(len(parts) == 3)

            phone_number = re.sub('\+|\(|\)|-| ', '', parts[0])
            assert(re.match('^\d{10,10}$', phone_number))

            questions = re.sub(' ', '', parts[1]).split('|')
            assert(all([re.match('\d+', q) for q in questions]))

            times = parts[2].split('|')
            assert(len(questions) == len(times))

            # schedule_questions(phone_number, questions, times)


def _schedule_process_json(json):
    pass


def _schedule_process(data):
    phone_number = data.get('phone-number')
    question_id = data.get('question-id')
    time = data.get('time')

    schedule_questions(phone_number, [question_id], [time])
    

def schedule_questions(phone_number, question_ids, times):
    # user = find_user_by(phone_number=phone_number)
    # if user is None:
    #     user = create_user(phone_number)

    for question_id, time in zip(question_ids, times):
        time = parse_time(time)
        schedule_question(phone_number, question_id, time)


def parse_time(time):
    return time


def schedule_question(phone_number, question_id, time):
    sq = ScheduledQuestion(phone_number, question_id, time)
    db.session.add(sq)
    db.session.commit()
    
