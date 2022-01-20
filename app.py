from email import message
import logging
import os
import re

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from helpers.stateChecker import *
from states.normalState import *
from states.cseEventState import *
from states.triviaState import *
from helpers.compare import *
from states.hangmanState import *

load_dotenv()

SOCKET_TOKEN = os.environ["SOCKET_TOKEN"]
SLACK_TOKEN = os.environ["SLACK_TOKEN"]
WEATHER_KEY = os.environ["WEATHER_KEY"]


app = App(token=SLACK_TOKEN, name="ben")
logger = logging.getLogger(__name__)

totalMessages = 0

@app.message(re.compile(""))
def anything(message, say):
    global totalMessages
    channel_type = message["channel_type"]
    if channel_type != "im":
        return
    user_id = message["user"]
    dm_channel = message["channel"]
    currentState = checkState(user_id)
    totalMessages +=1
    if compareValues(message['text'], 'usage'):
        say(text=str(totalMessages), channel=dm_channel)

    elif currentState == "normal":
        commenceNormalState(message, say)
    elif currentState == "trivia":
        commenceTriviaState(message, say)
    elif currentState == "hangman":
        commenceHangmanState(message, say)
    elif currentState == "studyTable":
        commenceStudyTableState(message, say)
    elif currentState == "cseEvent":
        commenceCSEEvent(message, say)

def main():
    handler = SocketModeHandler(app, SOCKET_TOKEN)
    handler.start()

if __name__ == "__main__":
    main()