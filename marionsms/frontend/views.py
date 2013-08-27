# -*- coding: utf-8 -*-
import string
from collections import defaultdict
from flask import (Blueprint, render_template, current_app, request, json,
                   flash, url_for, redirect, session, abort, make_response)
from flask.ext.login import current_user, login_user, logout_user, login_required

from ..notifier import send_nows_smss
import marionsms.scheduler as s
from ..extensions import db
from ..models import Message, ScheduledMessage, Response, User



DAYS_OF_WEEK = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                'saturday', 'sunday']


frontend = Blueprint('frontend', __name__)


@frontend.route('/')
def landing_page():
    return render_template('landing.html')
    

@frontend.route('/login', methods=['POST'])
def login():
    username = request.values.get('username')
    password = request.values.get('password')
    user = User.query.filter_by(username=username).first()
    current_app.logger.info('LOGIN {} trying to log in...'.format(username))
    if user and user.verify_password(password):
        current_app.logger.info('LOGIN {} logged in successfully'.format(username))
        login_user(user)
        flash("Welcome back, {}!".format(username), 'success')
        return redirect(request.args.get("next") or url_for(".home"))
    current_app.logger.info('LOGIN {} failed at logging in.'.format(username))
    flash("Incorrect username or password; please try again.".format(username), 'warning')
    return redirect(url_for('.landing_page'))


@frontend.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    current_app.logger.info('LOGOUT logged out {}.'.format(current_user.username))
    logout_user()
    flash("You've been logged out.")
    return redirect(url_for('.landing_page'))


@frontend.route('/home')
@login_required
def home():
    return render_template('home.html')


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


@frontend.route('/schedule', methods=['POST', 'GET', 'DELETE'])
@login_required
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
@login_required
def generate_report_csv():
    start_date = request.values.get('start-date')
    end_date = request.values.get('end-date')
    responses = Response.query.filter(Response.answered_at.between(start_date, end_date)).all()

    csv = responses_to_csv(responses)
    response = make_response(csv)
    response.headers['Content-Type'] = 'text/csv'
    return response


@frontend.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    responses = Response.query.order_by(Response.answered_at.desc()).all()
    return render_template('report.html', 
                           responses=responses)


@frontend.route('/messages', methods=['GET', 'POST', 'DELETE'])
@login_required
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


@frontend.route('/demo', methods=['GET', 'POST'])
@login_required
def demo():
    if request.method == 'POST':
        current_app.logger.info("SENDING TEXTS... (from /demo)")
        send_nows_smss()
    return render_template('demo.html')
