from app import *
from states.normalState import *
from helpers.compare import *
from pytrivia import Category, Diffculty, Type, Trivia
import random

triviaAnswer={}
triviaAnswering = {}

my_api = Trivia(True)

def commenceTriviaState(message, say):
    channel_type = message["channel_type"]
    dm_channel = message["channel"]
    user_id = message["user"]

    if user_id not in triviaAnswering.keys() or triviaAnswering[user_id] == False:
        triviaAnswering[user_id] = True
        response = my_api.request(1)
        say(text=response['results'][0]['question'], channel=dm_channel)
        if response['results'][0]['type'] == 'boolean':
            if response['results'][0]['correct_answer'] == True:
                triviaAnswer[user_id] = 'A'
            else:
                triviaAnswer[user_id] = 'B'
            say(text="A: True", channel=dm_channel)
            say(text="B: False", channel=dm_channel)
        else:
            possibleAnswers=response['results'][0]['incorrect_answers']
            possibleAnswers.append(response['results'][0]['correct_answer'])
            random.shuffle(possibleAnswers)
            if possibleAnswers.index(response['results'][0]['correct_answer']) == 0:
                triviaAnswer[user_id] = 'A'
            elif possibleAnswers.index(response['results'][0]['correct_answer']) == 1:
                triviaAnswer[user_id] = 'B'
            elif possibleAnswers.index(response['results'][0]['correct_answer']) == 2:
                triviaAnswer[user_id] = 'C'
            else:
                triviaAnswer[user_id] = 'D'
            say(text='A: ' + possibleAnswers[0], channel=dm_channel)
            say(text='B: ' + possibleAnswers[1], channel=dm_channel)
            say(text='C: ' + possibleAnswers[2], channel=dm_channel)
            say(text='D: ' + possibleAnswers[3], channel=dm_channel)

    else:
        if compareValues(message['text'].upper(), triviaAnswer[user_id]):
            say(text='Correct!', channel=dm_channel)
            changeState(user_id, 'normal')
        else:
            say(text='Incorrect.', channel = dm_channel)
            response = "The correct answer was *" + triviaAnswer[user_id] + "*"
            say(text=response, channel=dm_channel)
        say(text='Thanks for playing!', channel=dm_channel)
        changeState(user_id, 'normal')
        triviaAnswering[user_id] = False