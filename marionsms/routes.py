from flask import Flask, jsonify, redirect, url_for, render_template



API_VERSION = 'v1.0'


app = Flask(__name__)



@app.route('/')
def landing_page():
    app.logger.info('hurr')
    return render_template('landing-page.html')


# require login
@app.route('/home', methods=['POST'])
def home():
    return render_template('home.html')
    

@app.route('/login', methods=['POST', 'GET'])
def login():
    # login(request)
    app.logger.info('wtf?????')
    return redirect(url_for('home'))


@app.route('/logout', methods=['POST'])
def logout():
    # logout(request)
    return redirect(url_for('landing_page'))


# require login
@app.route('/schedule')
def schedule():
    return render_template('schedule.html')


# require login
@app.route('/reports')
def report():
    return render_template('report.html')



################################################################################
#                                  API                                         #
################################################################################
def api_route(verb):
    api_prefix = '/api/' + API_VERSION
    return api_prefix + '/' + verb

###############################################
#                Questions                    #
###############################################
@app.route(api_route('questions'))
def questions():
    questions = []
    return jsonify({'questions' : questions})


@app.route(api_route('questions'), methods=['POST'])
def create_question():
    # question = db.create_question()
    # ?? what do i do here again?


@app.route(api_route('question/<int:question_id>'))
def get_question():
    # question = find_question(question_id)
    # return jsonify({'question' : question})


###############################################
#                Scheduling                   #
###############################################
@app.route(api_route('schedule'))
def schedule():
    rows = []
    return jsonify({'schedule' : rows})


@app.route(api_route('schedule'), methods=['POST'])
def add_to_schedule():
    # data = get_csv_or_json
    # append_to_schedule(data)
    # ?? what do i do here again?


@app.route(api_route('schedule/<phone_number>'), methods=['DELETE'])
def remove_number_from_schedule(phone_number):
    # remove_from_schedule(phone_number)
    # ?? what do i do here again?


# @app.route(api_route('schedule/<phone_number>'), methods=['PUT'])
# def remove_number_from_schedule(phone_number):
#     # edit... blah blah blah(phone_number)
#     # ?? what do i do here again?


###############################################
#                Scheduling                   #
###############################################
@app.route(api_route('report'))
def report():
    rows = []
    return jsonify({'report' : rows})
