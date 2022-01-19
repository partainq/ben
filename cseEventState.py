from bolt_socket import *
from normalState import *
from stateChecker import *
from helpfulFunctions import *

password = 'admin'
userPassword={}
nextCSEEvent = ''

def commenceCSEEvent(message, say):
    global nextCSEEvent
    dm_channel = message["channel"]
    user_id = message["user"]

    if user_id not in userPassword.keys():
        userPassword[user_id] = False

    if message['text'] == password:
        userPassword[user_id] = True
        say(text='Please enter event name followed by date seperated by ; (ex. Game Jam;4/15/21', channel=dm_channel)

    if userPassword[user_id] == True:
        if message['text'] == password:
            return
        elif ';' in message['text']:
            say(text='Next cse event has been changed', channel=dm_channel)
            nextCSEEvent = message['text']
            print(nextCSEEvent)
            changeState(user_id, 'normal')
        elif message['text'] == 'quit':
            changeState(user_id, 'normal')
        else:
            say(text='try again', channel=dm_channel)
    elif message['text'] == 'quit':
        changeState(user_id, 'normal')
    else:
        say(text='wrong password', channel=dm_channel)
        changeState(user_id, 'normal')

def getNextCSEEvent():
    if len(nextCSEEvent) > 0:
        return nextCSEEvent
    else:
        return "nope"