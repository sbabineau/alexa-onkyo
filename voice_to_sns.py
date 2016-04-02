from __future__ import print_function

import boto3


SQS = boto3.resource('sqs')
QUEUE = SQS.Queue('https://sqs.us-east-1.amazonaws.com/711570343235/alexa-onkyo')
SOURCE_DICT = {
    'aux': 'aux1',
    'auxillary': 'aux1',
    'off': 'standby',
    'b.d.': 'bd',
    'c.d.': 'tv',
    'd.v.d.': 'bd',
    'echo': 'pc',
    'p.c.': 'pc',
    't.v.': 'tv',
    'u.s.b.': 'usb',
    'network': 'net',
}


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

    return send_response()


def set_intent(intent):
    source = intent['slots']['Source']['value'].lower()
    source = SOURCE_DICT.get(source, source)
    if source in ('on', 'standby'):
        body = 'main.system-power={}'.format(source)
    else:
        body = 'main.input-selector={}'.format(source)
    QUEUE.send_message(MessageBody=body)


def send_response():
    return {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': 'ok'
            }
        }
    }
