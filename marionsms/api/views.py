# -*- coding: utf-8 -*-
from flask import (Blueprint, render_template, current_app, request,
                   flash, url_for, redirect, session, abort, jsonify)



API_VERSION = 'v1.0'
api = Blueprint('api', __name__)



################################################################################
#                                  API                                         #
################################################################################
def api_route(verb):
    api_prefix = '/api/' + API_VERSION
    return api_prefix + '/' + verb

###############################################
#                Questions                    #
###############################################
@api.route(api_route('questions'))
def questions():
    questions = []
    return jsonify({'questions' : questions})


@api.route(api_route('questions'), methods=['POST'])
def create_question():
    # question = db.create_question()
    # ?? what do i do here again?
    pass


@api.route(api_route('question/<int:question_id>'))
def get_question():
    # question = find_question(question_id)
    # return jsonify({'question' : question})
    pass


###############################################
#                Scheduling                   #
###############################################
@api.route(api_route('schedule'))
def schedule():
    rows = []
    return jsonify({'schedule' : rows})


@api.route(api_route('schedule'), methods=['POST'])
def add_to_schedule():
    # data = get_csv_or_json
    # append_to_schedule(data)
    # ?? what do i do here again?
    pass


@api.route(api_route('schedule/<phone_number>'), methods=['DELETE'])
def remove_number_from_schedule(phone_number):
    # remove_from_schedule(phone_number)
    # ?? what do i do here again?
    pass


# @api.route(api_route('schedule/<phone_number>'), methods=['PUT'])
# def remove_number_from_schedule(phone_number):
#     # edit... blah blah blah(phone_number)
#     # ?? what do i do here again?


###############################################
#                Scheduling                   #
###############################################
@api.route(api_route('report'))
def report():
    rows = []
    return jsonify({'report' : rows})
