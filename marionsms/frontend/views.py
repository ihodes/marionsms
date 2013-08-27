# -*- coding: utf-8 -*-
import string
from collections import defaultdict
from flask import (Blueprint, render_template, current_app, request, json,
                   flash, url_for, redirect, session, abort, make_response)


from ..notifier import send_nows_smss
import marionsms.scheduler as s
from ..extensions import db
from ..models import Message, ScheduledMessage, Response



DAYS_OF_WEEK = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                'saturday', 'sunday']


frontend = Blueprint('frontend', __name__)


@frontend.route('/')
def landing_page():
    return render_template('landing.html')


# require login
@frontend.route('/home')
def home():
    return render_template('home.html')
    

@frontend.route('/login', methods=['POST'])
def login():
    current_app.logger.info('Logging in...')
    # TK TODO
    return redirect(url_for('.home'))


@frontend.route('/logout', methods=['POST', 'GET'])
def logout():
    current_app.logger.info('Logging out...')
    # TK TODO
    return redirect(url_for('.landing_page'))


def _get_schedule():
    schedule = defaultdict(list)
    for scheduled_message in ScheduledMessage.query.all():
        if scheduled_message.active and not scheduled_message.message.hidden:
            schedule[scheduled_message.phone_number].append(scheduled_message)
    return schedule


def _process_csv(csv_file):
    msgs = []
    for line in csv_file:
        vals = line.split(',')
        vals = [string.strip(v) for v in vals]
        sm = s.schedule(*vals)
        msgs.append(sm)
        db.session.add(sm)
        current_app.logger.info("Scheduled: "+str(sm))
    db.session.commit()
    return msgs


# require login
@frontend.route('/schedule', methods=['POST', 'GET', 'DELETE'])
def schedule():
    if request.method == 'POST':
        csv = request.files.get('schedule-file')
        if csv:
            msgs = _process_csv(csv)
            flash('Scheduled {} messages.'.format(len(msgs)), 'info')
        else:
            sm = s.schedule(request.form.get('phone-number'),
                            request.form.get('message-id'),
                            request.form.get('frequency'),
                            request.form.get('time'))
            flash('Scheduled message \"{}\"  for {}'.format(sm.message.name,
                                                            sm.phone_number)
                  , 'info')
        return redirect(url_for('.schedule'))
    elif request.method == 'DELETE':
        smid = request.values.get('scheduled_message_id')
        sm = ScheduledMessage.query.get(smid)
        name = sm.message.name
        phone_number = sm.phone_number
        sm.active = False
        db.session.add(sm)
        db.session.commit()
        flash('Removed message \"{}\"  scheduled for {}'.format(name, phone_number),
              'warning')
        return redirect(url_for('.schedule'))
    return render_template('schedule.html',
                           schedule=_get_schedule(), 
                           DAYS_OF_WEEK=DAYS_OF_WEEK)


def responses_to_csv(responses):
    csv = ''
    for response in responses:
        csv += response.phone_number
        csv += ','
        csv += str(response.answered_at)
        csv += ','
        csv += str(response.message_id)
        csv += ','
        csv += ("\""+response.text+"\"")
        csv += '\n'

    return csv


@frontend.route('/report.csv')
def generate_large_csv():
    start_date = request.values.get('start-date')
    end_date = request.values.get('end-date')
    responses = Response.query.filter(Response.answered_at.between(start_date, end_date)).all()

    csv = responses_to_csv(responses)
    response = make_response(csv)
    response.headers['Content-Type'] = 'text/csv'
    return response


# require login
@frontend.route('/report', methods=['GET', 'POST'])
def report():
    responses = Response.query.order_by(Response.answered_at.desc()).all()
    return render_template('report.html', 
                           responses=responses)


# require login
@frontend.route('/messages', methods=['GET', 'POST', 'DELETE'])
def messages():
    if request.method == 'POST':
        m = Message(request.form['name'], request.form['text'])
        db.session.add(m)
        db.session.commit()
        flash('Created message \"{}\"'.format(m.name), 'info')
        return redirect(url_for('.messages'))
    elif request.method == 'DELETE':
        message_id = request.values.get('message_id')
        m = Message.query.get(message_id)
        name = m.name
        m.hidden = True
        db.session.add(m)
        db.session.commit()
        flash('Removed message \"{}\"'.format(name), 'warning')
        return redirect(url_for('.messages'))
    return render_template('messages.html', messages=Message.query.filter_by(hidden=False).all())


# require login
@frontend.route('/demo', methods=['GET', 'POST'])
def demo():
    if request.method == 'POST':
        current_app.logger.info("SENDING TEXTS... (from /demo)")
        send_nows_smss()
    return render_template('demo.html')
