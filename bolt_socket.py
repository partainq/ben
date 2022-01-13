import logging
import os
import re

import random
import pyjokes
import requests, json
import formats.weather, formats.help, formats.nextSemester

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from stateChecker import *
from normalState import *
from triviaState import *
from helpfulFunctions import *


load_dotenv()

SOCKET_TOKEN = os.environ["SOCKET_TOKEN"]
SLACK_TOKEN = os.environ["SLACK_TOKEN"]
WEATHER_KEY = os.environ["WEATHER_KEY"]


app = App(token=SLACK_TOKEN, name="ben")
logger = logging.getLogger(__name__)

@app.message(re.compile(""))
def anything(message, say):
    channel_type = message["channel_type"]
    if channel_type != "im":
        return
    user_id = message["user"]

    currentState = checkState(user_id)

    if currentState == "normal":
        commenceNormalState(message, say)
    elif currentState == "trivia":
        commenceTriviaState(message, say)


def main():
    handler = SocketModeHandler(app, SOCKET_TOKEN)
    handler.start()

if __name__ == "__main__":
    main()