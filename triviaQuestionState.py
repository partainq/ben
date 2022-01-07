from app import *
from stateChecker import *

# triviaAnswer = {channel_id: answer}
triviaAnswer = {}


def commenceTriviaQuestionState(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    text = event.get('text')

    if text == triviaAnswer[channel_id]:
        client.chat_postMessage(channel=channel_id, text='Correct!')
    else:
        client.chat_postMessage(channel=channel_id, text='Incorrect!')
        client.chat_postMessage(channel=channel_id, text="The correct answer was:")
        client.chat_postMessage(channel=channel_id, text=triviaAnswer[channel_id])
    changeState(channel_id, 'normalState')
    client.chat_postMessage(channel=channel_id, text='Thanks for playing with me :)')




def triviaAnswer(channel_id, answer):
    triviaAnswer[channel_id] = answer