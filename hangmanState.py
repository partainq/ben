import random


hangmanWords=["computer", "apples", "psychic"]
currentHangman={}
numLives = {}
currentProgress = {}
# currentHangman={user_id: word}


def commenceHangmanState(message, say):
    channel_type = message["channel_type"]
    dm_channel = message["channel"]
    user_id = message["user"]

    if user_id not in currentHangman.keys():
        currentHangman[user_id] = random.choice(hangmanWords)
        numLives[user_id] = 5
        currentProgress[user_id] = ''
        for x in range(len(currentHangman[user_id])):
            currentProgress[user_id] = currentProgress[user_id] + "_"

    else:
        if message['text'] in currentHangman[user_id] and message['text'] not in currentProgress[user_id]:
            say(text="correct", channel=dm_channel)
            index = currentHangman[user_id].indexof(message['text'])
            currentProgress = currentProgress[user_id][:index] + message["text"] + currentProgress[user_id][index+1:]
        else:
            say(text="incorrect", channel=dm_channel)
            numLives[user_id] -= 1

    lives= str(numLives[user_id]) + " lives"
    say(text=lives, channel=dm_channel)
    print(currentProgress[user_id])
    say(text=currentProgress[user_id], channel=dm_channel)
    say(text="Make Guess", channel=dm_channel)




