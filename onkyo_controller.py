import atexit

import boto3
from eiscp import eISCP


def main(receiver):
    sqs = boto3.resource('sqs', region_name='us-east-1')
    queue = sqs.Queue('https://sqs.us-east-1.amazonaws.com/711570343235/alexa-onkyo')
    while True:
        message = queue.receive_messages(WaitTimeSeconds=10)
        try:
            message = message[0]
            body = message.body
            receiver.command(body)
            message.delete()
        except:
            continue


def goodbye(receiver):
    """Gracefully disconnects"""
    receiver.disconnect()


if __name__ == '__main__':
    receiver = eISCP('192.168.0.111')
    atexit.register(goodbye, receiver)
    main(receiver)

