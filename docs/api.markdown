# Information Overview
This section serves as an overview of the different types of data returned and accepted by MarionSMS.

## Phone Numbers
Phone numbers are expected to be 9 digit numbers. No other validation is performed on phone numbers. The characters " ", "-", "+", ")", and "(" are stripped out automatically, but letters and other non-digit characters will cause the number not to validate.

## Question IDs
Question ids are always integers. Any other characters in a question will cause the question not to validate.

## Question Text
Questions can be of length 160 ASCII characters.

## Times
[TK TODO how to handle DST?]
 
Times represent the time (and date or frequency) an associated question will be send to the user. Questions are sent out every hour only, (e.g. a question scheduled for 10:07 would be sent out at 11:00).

Times should be of the format: 

TIME (FREQUENCY optional) (DATE optional)

TIME should to be in UTC+00:00 unless a valid offset is included. Times should be in ISO 940 (TK??) format (e.g. 17:23 UTC+00:00), as should associated dates if a date is desired. 

FREQUENCY should be daily, weekly, monthly, or yearly.

If both a FREQUENCY and a DATE are included, the question will not be sent out until on or after that given DATE, and then will continue to be sent out at the given FREQUENCY after that.

If just a FREQUENCY is provided, the question will be sent out as soon as it is TIME, and in perpetuity after that.

If just a DATE is provided, the question will be sent out at TIME on that DATE only, and never again.

If just a TIME is provided, questions will be sent out daily at that time.

Examples:

Qs sent out at 3PM EST daily starting on the 1st of December, 2013
10:00+05:00EST daily 01-12-2013

Qs sent out every 7 days at 5PM, starting o the 27th of June
17:00 weekly 27-06-2014

Qs sent out every day at 5AM
5:00



# The API
This section details our API, which is also used internally. All questions should include an API token associated with your account.




# Questions
Before questions can be sent out, they must be created. This endpoint is used to view existing questions and create new questions.


## /api/1.0/questions
### GET
Returns CSV of all questions and their integer IDs.

Format: QUESTION ID, QUESTION TEXT

### POST
Create a new question. 

(TK ?? can POST 'return' date?) Returns the question id.


## /api/1.0/questions/<id>
### GET
Returns the text of the question.




# Scheduling
Questions must be scheduled for a given phone number, at certain times and at certain frequencies. This endpoint is where you can do that, as well as reschedule and deschedule existing questions.


## /api/1.0/schedule
### GET
Returns a CSV of the current schedule. This is in the same format as is accepted in POST, below.


### POST 
Schedule question(s) for phone numbers. Can add questions & times, or entirely new phone numbers. 

POST body must be CSV data with the following columns in the given order. There must be no header-line. 

```
phone_number = valid 9-digit number
question ids = |-separated list of question id to schedule
times = |-separated list of times the associated question should be scheduled for
optional = name associated with number
id = internal id you would like to associated with the number
note = any small note you would like to include
```

If a phone number already exists, new questions and times will be added to that number's schedule.


## /api/1.0/schedule/<phone_number>
### DELETE
Remove a phone number from the schedule, effectively removing all scheduled questions. This will not remove the data already collected which is associated with the number. 


### PUT
Update an existing phone number's schedule. 

#### Params
all of:
* [required] question (the number of the question being edited)
* [required] time (the time of the question being edited)

and one of:
* [optional] new_time (the new time of the question being edited)
* [optional] remove (= true) to unschedule the question




# Reporting
Data collected is accessible from this endpoint. 


## /api/1.0/report
### GET
