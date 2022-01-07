import slack
import os
import random
import requests
import json

from stateChecker import *
from normalState import *
from triviaQuestionState import *
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter



env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events', app)
#slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events', app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
#client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

BOT_ID = client.api_call('auth.test')['user_id']


@slack_event_adapter.on('message')
def message(payload):


    flag = True
    event = payload.get('event', {})
    channel_id = event.get('channel')
    currentState = checkState(channel_id)
    if currentState == 'normal':
        commenceNormalState(payload)
    elif currentState == "triviaQuestionState":
        commenceTriviaQuestionState(payload)
    # user_id = event.get('user')
    # text = event.get('text')
    #
    # if text[-1] == "=":
    #     numbers = text.split()
    #     flag = False
    #     if numbers[1] == "-":
    #         client.chat_postMessage(channel=channel_id, text=int(numbers[0]) - int(numbers[2]))
    #     if numbers[1] == "*":
    #         client.chat_postMessage(channel=channel_id, text=int(numbers[0]) * int(numbers[2]))
    #     if numbers[1] == "+":
    #         client.chat_postMessage(channel=channel_id, text=int(numbers[0]) + int(numbers[2]))
    #
    # elif "flip a coin" in text.lower():
    #     channel_id = event.get("channel")
    #     rand_int = random.randint(0, 1)
    #     if rand_int == 0:
    #         results = "Heads"
    #     else:
    #         results = "Tails"
    #     message = "The result is "+results
    #
    #     client.chat_postMessage(channel=channel_id, text=message)
    #
    # elif user_id != BOT_ID and "weather" in text.lower():
    #     weather_key = "32843bad9e96bb36c7935458544b1628"
    #     lat = "48.208176"
    #     lon = "16.373819"
    #     url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, weather_key)
    #     #response = requests.get(url)
    #     #data = json.loads(response.text)
    #     client.chat_postMessage(channel=channel_id, text="weather")
    #
    # elif user_id != BOT_ID and flag == True:
    #     client.chat_postMessage(channel=channel_id, text=text)

if __name__ == "__main__":
    app.run(debug=True)