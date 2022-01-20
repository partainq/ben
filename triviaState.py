from bolt_socket import *
from normalState import *
from helpfulFunctions import *
from pytrivia import Category, Diffculty, Type, Trivia
import random

triviaList = [["When was Taylor founded?", "1846"], ["Who made me?", "Quinn Partain and Micah Odell"],
              ["What does DTR mean?", "Define the relationship"], ["When was the 1984 Ford invented?", "1984"]]
triviaAnswer={}
# triviaAnswer = {user_id: answer}
triviaAnswering = {}
# triviaAnswering = {user_id: True}

my_api = Trivia(True)


def commenceTriviaState(message, say):
    channel_type = message["channel_type"]
    dm_channel = message["channel"]
    user_id = message["user"]

    if user_id not in triviaAnswering.keys() or triviaAnswering[user_id] == False:
        triviaAnswering[user_id] = True
        response = my_api.request(1)
        # say(text=response['results'][0]['question'], channel=dm_channel)
        # say(text=response['results'][0]['correct_answer'], channel=dm_channel)
        # question = random.choice(triviaList)
        triviaAnswer[user_id] = response['results'][0]['correct_answer']
        # say(text="I love trivia", channel=dm_channel)
        # say(text="lets play trivia", channel=dm_channel)
        say(text=response['results'][0]['question'], channel=dm_channel)
        if response['results'][0]['type'] == 'boolean':
            say(text="True", channel=dm_channel)
            say(text="False", channel=dm_channel)
        else:
            possibleAnswers=response['results'][0]['incorrect_answers']
            possibleAnswers.append(response['results'][0]['correct_answer'])
            random.shuffle(possibleAnswers)
            say(text=possibleAnswers[0], channel=dm_channel)
            say(text=possibleAnswers[1], channel=dm_channel)
            say(text=possibleAnswers[2], channel=dm_channel)
            say(text=possibleAnswers[3], channel=dm_channel)

    else:
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