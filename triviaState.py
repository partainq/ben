from bolt_socket import *
from normalState import *
from helpfulFunctions import *
import random

triviaList = [["do birds have heads?", "yes"], ["is Snape evil?", "no"]]
triviaAnswer={}
# triviaAnswer = {user_id: answer}
triviaAnswering = {}
# triviaAnswering = {user_id: True}


def commenceTriviaState(message, say):
    channel_type = message["channel_type"]
    dm_channel = message["channel"]
    user_id = message["user"]

    if user_id not in triviaAnswering.keys() or triviaAnswering[user_id] == False:
        triviaAnswering[user_id] = True
        question = random.choice(triviaList)
        triviaAnswer[user_id] = question[1]
        # say(text="I love trivia", channel=dm_channel)
        # say(text="lets play trivia", channel=dm_channel)
        say(text=question[0], channel=dm_channel)
    else:
        print(message['text'], triviaAnswer[user_id])
        if compareValues(message['text'], triviaAnswer[user_id]):
            say(text='Correct!', channel=dm_channel)
            changeState(user_id, 'normal')
        else:
            say(text='Incorrect', channel = dm_channel)
            response = "The correct answer was "+ triviaAnswer[user_id]
            say(text=response, channel=dm_channel)
        say(text='Thanks for playing', channel=dm_channel)
        changeState(user_id, 'normal')
        triviaAnswering[user_id] = False






# def triviaAnswer(channel_id, answer):
#     triviaAnswer[channel_id] = answer