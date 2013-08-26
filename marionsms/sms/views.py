# -*- coding: utf-8 -*-
from flask import (Blueprint, render_template, current_app, request, json,
                   flash, url_for, redirect, session, abort, make_response)

from ..extensions import db
from ..models import ScheduledMessage, Response


sms = Blueprint('sms', __name__, url_prefix="/sms")


@sms.route('/receive', methods=['POST'])
def receive():
    # TK TODO validate with Twilio.validate, process answer (or test for HELP or equivalent)
    from_ = request.form.get('From')
    response_text = request.form.get('Body')

    current_app.logger.info("Incoming text from {}: {}".format(from_, response_text))
    
    scheduled_messages = ScheduledMessage.query.filter_by(phone_number=from_)
    ordered_sms = scheduled_messages.order_by(ScheduledMessage.last_sent.desc())

    for sm in ordered_sms:
        if sm.last_sent: # make sure it was sent
            response = Response(from_, response_text, sm.message_id, sm.id)
            db.session.add(response)
            db.session.commit()
            break
    
    
    

    return "recieved"
