from __future__ import print_function

import boto3


SQS = boto3.resource('sqs')
QUEUE = SQS.Queue('https://sqs.us-east-1.amazonaws.com/711570343235/alexa-onkyo')


def lambda_handler(event, context):

    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")
    if event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    if intent_name == 'set':
        set_intent(intent)


def set_intent(intent):
    QUEUE.send_message(body='main.input-selector={}'.format(intent['slots']['Source']['value']))
