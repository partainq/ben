from bolt_socket import *
from normalState import *
from helpfulFunctions import *
import formats.studyTable


explaining = True
asking = False
confirming = False
reasoning = False
who = ''

def commenceStudyTableState(message, say):
    global explaining, asking, confirming, reasoning, who

    channel_type = message["channel_type"]
    dm_channel = message["channel"]
    user_id = message["user"]

    if message['text'] == 'quit':
        say(text="studyTable state cancel", channel=dm_channel)
        changeState(user_id, 'normal')
    
    elif explaining:
        msg = "*Study Table*\n I will walk you through a series of questions to help setup a study table anonymously. At any point you may type *quit* and the process will be terminated. Should issues arrise, the CSE department could view message history. Please use _wisely_ and be _polite_.\n"
        say(text=msg, channel=dm_channel)
        say(text="What professor would you like to notify? Please use an @sign ", channel=dm_channel)
        explaining = False
        asking = True
    elif asking:
        who = message['text']
        if (who[0:2] == "<@"):
            msg = "Are you sure you want to notify " + who + " for a study table? Please respond with a *yes* or *no*."
            say(text=msg, channel=dm_channel)
            confirming = True
            asking = False
        else:
            say(text="Incorrect username format. Please use the @sign and specify who you would like to be notifed", channel=dm_channel)
            say(text="What professor would you like to notify? Please use an @sign ", channel=dm_channel)
    elif confirming:
        if message['text'] == 'yes':
            msg = "Great! Please provide a short reason for this study table and the class that it is for.\n\n*Example:*\nCOS243 Javascript help with promises."
            say(text=msg, channel=dm_channel)
            confirming = False
            reasoning = True
        else:
            say(text="Incorret format, please respond with a 'yes' or 'no'.")
            msg = "Are you sure you want to notify " + who + " for a study table? Please respond with a 'yes' or 'no'."
            say(text=msg, channel=dm_channel)
    elif reasoning:
        msg = 'An anonymous request for a study table has been sent to '+ who +'. Good luck in your studies!'
        say(text=msg, channel=dm_channel)

        id = who[2:-1]
        blocks = formats.studyTable.getFormat(message['text'])
        say(blocks=blocks, text="study table alert", channel=id)
        changeState(user_id, 'normal')


