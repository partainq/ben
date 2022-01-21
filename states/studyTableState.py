from app import *
from states.normalState import *
from helpers.compare import *
from helpers.stateChecker import *
import formats.studyTable

explaining = {}
asking = {}
confirming = {}
reasoning = {}
who = ''
history = {}
checkingPassword = {}
findingBadMessage = {}
password = '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918'

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
        checkingPassword[user_id] = False
        findingBadMessage[user_id] = False

    if message['text'].lower() == 'quit':
        say(text="studyTable state cancel", channel=dm_channel)
        del reasoning[user_id]
        del explaining[user_id]
        del asking[user_id]
        del confirming[user_id]
        del checkingPassword[user_id]
        del findingBadMessage[user_id]
        changeState(user_id, 'normal')

    elif message['text'].lower() == 'check history':
        say(text="To check history, please provide admin password", channel=dm_channel)
        checkingPassword[user_id] = True
        explaining[user_id] = False
        asking[user_id] = False
        confirming[user_id] = False
        reasoning[user_id] = False
        findingBadMessage[user_id] = False

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
        if user_id in history.keys():
            history[user_id].append(message['text'])
        else:
            history[user_id] = [message['text']]

        id = who[2:-1]
        blocks = formats.studyTable.getFormat(message['text'])
        say(blocks=blocks, text="study table alert", channel=id)
        del reasoning[user_id]
        del explaining[user_id]
        del asking[user_id]
        del confirming[user_id]
        del checkingPassword[user_id]
        changeState(user_id, 'normal')
    elif checkingPassword[user_id]:
        if hashlib.sha256(message['text'].encode()).hexdigest() == password:
            say(text='Please enter what was said.', channel=dm_channel)
            findingBadMessage[user_id] = True
            checkingPassword[user_id] = False
        else:
            say(text='Incorrect password, try again.', channel=dm_channel)
    elif findingBadMessage[user_id]:
        for x in history.keys():
            for y in history[x]:
                if compareValues(y, message['text']):
                    tempUser = '<@' + x + '>'
                    say(text='We found this *' + y + '* from ' + tempUser, channel=dm_channel)
                    say(text="Thank you.", channel=dm_channel)
                    del reasoning[user_id]
                    del explaining[user_id]
                    del asking[user_id]
                    del confirming[user_id]
                    del checkingPassword[user_id]
                    del findingBadMessage[user_id]
                    changeState(user_id, 'normal')
                    return
        say(text='No message explicitly matched *' + message['text'] +"*", channel=dm_channel)