# -*- coding: utf-8 -*-
from collections import defaultdict
import random
from flask import (Blueprint, render_template, current_app, request, json,
                   flash, url_for, redirect, session, abort, make_response)



import marionsms.scheduler as s
from ..extensions import db

from ..models import *



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


# require login
@frontend.route('/schedule', methods=['POST', 'GET'])
def schedule():
    if request.method == 'POST':
        is_csv = request.form.get('schedule-file', False)
        if is_csv:
            pass
        else:
            s.schedule(request.form)
        return redirect(url_for('.schedule'))
    schedule = defaultdict(list)
    for sq in ScheduledQuestion.query.all():
        q = Question.query.get(sq.question_id)
        schedule[sq.phone_number].append((q.text,
                                          q.name,
                                          sq.time))
    return render_template('schedule.html', schedule=schedule, r=random.random)


# require login
@frontend.route('/report')
def report():
    return render_template('report.html')


# require login
@frontend.route('/questions', methods=['GET', 'POST'])
def questions():
    if request.method == 'POST':
        q = Question(request.form['name'], request.form['text'])
        db.session.add(q)
        db.session.commit()
        return redirect(url_for('.questions'))
    return render_template('questions.html', questions=Question.query.all())
