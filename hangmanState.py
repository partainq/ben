import random
from stateChecker import *
import formats.hangman


hangmanWords=["psych", "roller", "wengatz", "olsen","chapel","brandle","samuel","morris","gerig","brew","english",
              "bergwall","campbell","euler","reade","metcalf","rupp","stu","loop","randall","apple","fruit","titanic",
              "batman","spiderman","thor","cars","fence","yeti","monkey","rhino","turtle","slack","hangman","lion",
              "tiger","zebra"]
currentHangman={}
numLives = {}
currentWord = {}
# currentHangman={user_id: word}


def commenceHangmanState(message, say):
    channel_type = message["channel_type"]
    dm_channel = message["channel"]
    user_id = message["user"]

    if user_id not in currentHangman.keys():
        currentHangman[user_id] = random.choice(hangmanWords)
        numLives[user_id] = 5
        currentWord[user_id] = ''
        say(text='let us begin', channel=dm_channel)
        for x in range(len(currentHangman[user_id])):
            currentWord[user_id] = currentWord[user_id] + "_"

    else:
        if len(message['text']) > 1:
            say(text="Please only guess one letter", channel=dm_channel)
            return
        elif ord(message['text']) < 65 or 90 < ord(message['text']) < 97 or 122 < ord(message['text']):
            say(text="Please guess an actual letter", channel=dm_channel)
            return
        elif message['text'].lower() in currentHangman[user_id] and message['text'] != "_":
            say(text="correct", channel=dm_channel)
            tempIndex = (currentHangman[user_id].lower()).index(message['text'])
            flag = True
            while flag == True:
                currentWord[user_id] = currentWord[user_id][:tempIndex] + message["text"] + currentWord[user_id][tempIndex+1:]
                currentHangman[user_id] = currentHangman[user_id][:tempIndex] + "_" + currentHangman[user_id][tempIndex+1:]
                if message['text'] in currentHangman[user_id]:
                    tempIndex = (currentHangman[user_id].lower()).index(message['text'])
                else:
                    flag = False


        else:
            say(text="incorrect", channel=dm_channel)
            numLives[user_id] -= 1
            if numLives[user_id] < 1:
                say(text="Out of lives", channel=dm_channel)
                say(text="The word was: " + currentWord[user_id], channel=dm_channel)
                say(text="Thanks for playing with me", channel=dm_channel)
                changeState(user_id, 'normal')
                del currentHangman[user_id]
                return

    if "_" not in currentWord[user_id]:
        say(text="The word was: " + currentWord[user_id], channel=dm_channel)
        say(text="you win", channel=dm_channel)
        changeState(user_id, 'normal')
        del currentHangman[user_id]
        return

    lives= str(numLives[user_id]) + " lives remaining"
    say(text="Make Guess", channel=dm_channel)
    blocks = formats.hangman.getFormat(numLives[user_id], currentWord[user_id])

    say(blocks=blocks, text="hangman", channel=dm_channel)




