from bolt_socket import *
from normalState import *
from helpfulFunctions import *
from stateChecker import *
import formats.studyTable


# explaining = True
explaining = {}
# asking = False
asking = {}
# confirming = False
confirming = {}
# reasoning = False
reasoning = {}
who = ''

def commenceStudyTableState(message, say):
    global explaining, asking, confirming, reasoning, who

    channel_type = message["channel_type"]
    dm_channel = message["channel"]
    user_id = message["user"]

    if user_id not in explaining.keys():
        explaining[user_id] = True
        asking[user_id] = False
        confirming[user_id] = False
        reasoning[user_id] = False

    if message['text'] == 'quit':
        say(text="studyTable state cancel", channel=dm_channel)
        del reasoning[user_id]
        del explaining[user_id]
        del asking[user_id]
        del confirming[user_id]
        changeState(user_id, 'normal')
    
    elif explaining[user_id]:
        msg = "*Study Table*\n I will walk you through a series of questions to help setup a study table anonymously. At any point you may type *quit* and the process will be terminated. Should issues arrise, the CSE department could view message history. Please use _wisely_ and be _polite_.\n"
        say(text=msg, channel=dm_channel)
        say(text="What professor would you like to notify? Please use an @sign ", channel=dm_channel)
        explaining[user_id] = False
        asking[user_id] = True
    elif asking[user_id]:
        who = message['text']
        if (who[0:2] == "<@"):
            msg = "Are you sure you want to notify " + who + " for a study table? Please respond with a *yes* or *no*."
            say(text=msg, channel=dm_channel)
            confirming[user_id] = True
            asking[user_id] = False
        else:
            say(text="Incorrect username format. Please use the @sign and specify who you would like to be notifed", channel=dm_channel)
            say(text="What professor would you like to notify? Please use an @sign ", channel=dm_channel)
    elif confirming[user_id]:
        if message['text'] == 'yes':
            msg = "Great! Please provide a short reason for this study table and the class that it is for.\n\n*Example:*\nCOS243 Javascript help with promises."
            say(text=msg, channel=dm_channel)
            confirming[user_id] = False
            reasoning[user_id] = True
        else:
            say(text="Incorret format, please respond with a 'yes' or 'no'.")
            msg = "Are you sure you want to notify " + who + " for a study table? Please respond with a 'yes' or 'no'."
            say(text=msg, channel=dm_channel)
    elif reasoning[user_id]:
        msg = 'An anonymous request for a study table has been sent to '+ who +'. Good luck in your studies!'
        say(text=msg, channel=dm_channel)

        id = who[2:-1]
        blocks = formats.studyTable.getFormat(message['text'])
        say(blocks=blocks, text="study table alert", channel=id)
        del reasoning[user_id]
        del explaining[user_id]
        del asking[user_id]
        del confirming[user_id]
        changeState(user_id, 'normal')


