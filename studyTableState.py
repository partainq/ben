from bolt_socket import *
from normalState import *
from helpfulFunctions import *


explaining = True
asking = False
confirming = False
who = ''

def commenceStudyTableState(message, say):
    global explaining, asking, confirming, who

    channel_type = message["channel_type"]
    dm_channel = message["channel"]
    user_id = message["user"]

    if message['text'] == 'quit':
        say(text="studyTable state cancel", channel=dm_channel)
        changeState(user_id, 'normal')
    
    if explaining:
        say(text="studyTable state is blah blah blah", channel=dm_channel)
        say(text="who would you like to notify? Please use an @sign ", channel=dm_channel)
        explaining = False
        asking = True
    elif asking:
        who = message['text']
        if (who[0:2] == "<@"):
            msg = "Are you sure you want to notify " + who + " for a study table? Please respond with a 'yes' or 'no'."
            say(text=msg, channel=dm_channel)
            confirming = True
            asking = False
        else:
            say(text="Incorrect username format. Please use the @ sign and specify who you would like to be notifed", channel=dm_channel)
            say(text="who would you like to notify? Please use an @sign ", channel=dm_channel)
    elif confirming:
        if message['text'] == 'yes':
            msg = 'An anonymous request for a study table has been sent to '+ who +'. Good luck in your studies!'
            say(text=msg, channel=dm_channel)
            id = who[2:-1]
            say(text="Hi", channel=id)
            changeState(user_id, 'normal')
        else:
            say(text="Incorret format, please respond with a 'yes' or 'no'.")
            msg = "Are you sure you want to notify " + who + " for a study table? Please respond with a 'yes' or 'no'."
            say(text=msg, channel=dm_channel)


