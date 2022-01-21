from app import *
from states.normalState import *
from helpers.stateChecker import *
from helpers.compare import *
import hashlib

password = '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918'
userPassword={}
nextCSEEvent = ''

def commenceCSEEvent(message, say):
    global nextCSEEvent
    dm_channel = message["channel"]
    user_id = message["user"]

    if user_id not in userPassword.keys():
        userPassword[user_id] = False

    if hashlib.sha256(message['text'].encode()).hexdigest() == password:
        userPassword[user_id] = True
        say(text='Please enter event name followed by date, then a message, seperated by *;* (ex. Game Jam;4/15/2022;Euler 217 with Dr. Denning)', channel=dm_channel)

    if userPassword[user_id] == True:
        if hashlib.sha256(message['text'].encode()).hexdigest() == password:
            return
        elif message['text'].count(';') == 2:
            say(text='Next CSE event has been changed.', channel=dm_channel)
            nextCSEEvent = message['text']
            print(nextCSEEvent)
            changeState(user_id, 'normal')
        elif message['text'].lower() == 'quit':
            say(text="back to normal Ben", channel=dm_channel)
            changeState(user_id, 'normal')
        else:
            say(text='Try again', channel=dm_channel)
    elif message['text'].lower() == 'quit':
        say(text="Thank you. Have a great day!", channel=dm_channel)
        changeState(user_id, 'normal')
    else:
        say(text='Incorrect password.', channel=dm_channel)
        changeState(user_id, 'normal')

def getNextCSEEvent():
    if len(nextCSEEvent) > 0:
        return nextCSEEvent
    else:
        return "Currently there is no CSE event added. To add an event, text *add cse event* to me and we can start that process."