import slack
import os
import random
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET_DEV'],'/slack/events', app)
#slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events', app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN_DEV'])
#client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

BOT_ID = client.api_call('auth.test')['user_id']

@slack_event_adapter.on('message')
def message(payload):
    flag = True
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

    if text[-1] == "=":
        numbers = text.split()
        flag = False
        if numbers[1] == "-":
            client.chat_postMessage(channel=channel_id, text=int(numbers[0]) - int(numbers[2]))
        if numbers[1] == "*":
            client.chat_postMessage(channel=channel_id, text=int(numbers[0]) * int(numbers[2]))
        if numbers[1] == "+":
            client.chat_postMessage(channel=channel_id, text=int(numbers[0]) + int(numbers[2]))

    elif "flip a coin" in text.lower():
        channel_id = event.get("channel")
        rand_int = random.randint(0, 1)
        if rand_int == 0:
            results = "Heads"
        else:
            results = "Tails"
        message = "The result is "+results

        client.chat_postMessage(channel=channel_id, text=message)

    elif user_id != BOT_ID and flag == True:
        client.chat_postMessage(channel=channel_id, text=text)

if __name__ == "__main__":
    app.run(debug=True)