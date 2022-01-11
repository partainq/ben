import logging
import os
import re
import random
import requests, json

import formats.weather, formats.help

from dotenv import load_dotenv
import pyjokes
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()

SOCKET_TOKEN_DEV = os.environ["SOCKET_TOKEN_DEV"]
SLACK_TOKEN_DEV = os.environ["SLACK_TOKEN_DEV"]
WEATHER_KEY = os.environ["WEATHER_KEY"]

app = App(token=SLACK_TOKEN_DEV, name="ben")
logger = logging.getLogger(__name__)


@app.message(re.compile("hi|hey|hello", re.I))
def greeting(message, say):
    channel_type = message["channel_type"]
    if channel_type != "im": 
        return

    dm_channel = message["channel"]
    user_id = message["user"]

    name = app.client.users_info(user=user_id)["user"]["name"]
    greeting = random.choice(["Hi there, ", "Hey, ", "Hello, ", "Great to hear from you, ", "Hi, "]) + name + "!"

    say(text=greeting, channel=dm_channel)

@app.message(re.compile("how are you|how is your day|how was your day|how are ya", re.I))
def question_greeting(message, say):
    channel_type = message["channel_type"]
    if channel_type != "im": #im = direct channel
        return

    dm_channel = message["channel"]
    user_id = message["user"]

    message = random.choice(["Having another day to help people is a blessing.", "Looks like my server is still up, so it is a good day!", "It's a good day to have a good day!", "Wonderful!"])

    say(text=message, channel=dm_channel)

@app.message(re.compile("whats up|what up|what's up|sup", re.I))
def casual_greeting(message, say):
    channel_type = message["channel_type"]
    if channel_type != "im": #im = direct channel
        return

    dm_channel = message["channel"]
    user_id = message["user"]

    message = random.choice(["Not much. Life is pretty quiet as a chatbot.", "Some movie about an old guy, balloons, and a flying house", "What can I help you with today?", "Great to hear from you."])

    say(text=message, channel=dm_channel)

@app.message(re.compile("joke", re.I))  # type: ignore
def random_joke(message, say):
    channel_type = message["channel_type"]
    if channel_type != "im": #im = direct channel
        return

    dm_channel = message["channel"]
    user_id = message["user"]

    joke = pyjokes.get_joke()
    say(text=joke, channel=dm_channel)

@app.message(re.compile("what are you|who are you|do you do|help|can you do|purpose|capabilities", re.I))
def help_message(message, say):
    channel_type = message["channel_type"]
    if channel_type != "im": #im = direct channel
        return

    dm_channel = message["channel"]
    user_id = message["user"]

    blocks = formats.help.getFormat()

    say(blocks=blocks, text="hi", channel=dm_channel)

@app.message(re.compile("flip a coin" or "coin flip", re.I))
def coin_flip(message, say):
    channel_type = message["channel_type"]
    if channel_type != "im":
        return
    
    dm_channel = message["channel"]
    rand_int = random.randint(0, 1)
    if rand_int == 0:
        results = "Coin Flip: heads"
    else:
        results = "Coin Flip: tails"

    say(text=results, channel=dm_channel)

@app.message(re.compile("weather", re.I))
def weather(message, say):
    channel_type = message["channel_type"]
    if channel_type != "im":
        return
    
    dm_channel = message["channel"]
    lat = "40"
    lon = "-85"

    url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=imperial" % (lat, lon, WEATHER_KEY)
    request = json.loads(requests.get(url).text)["current"]

    icon = request["weather"][0]['icon']
    temp = request["temp"]
    description= request["weather"][0]["main"]

    print(request)
    blocks = formats.weather.getFormat(temp, icon, description)

    say(blocks=blocks, text="weather", channel=dm_channel)

@app.message(re.compile("next semester|next term|classes next|next classes|next year", re.I))
def weather(message, say):
    channel_type = message["channel_type"]
    if channel_type != "im":
        return

    url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=imperial" % (lat, lon, WEATHER_KEY)
    request = json.loads(requests.get(url).text)["current"]

    icon = request["weather"][0]['icon']
    temp = request["temp"]
    description= request["weather"][0]["main"]
    dm_channel = message["channel"]

    print(request)
    blocks = formats.weather.getFormat(temp, icon, description)

    say(blocks=blocks, text="weather", channel=dm_channel)

@app.event("team_join")
def ask_for_introduction(event, say):
    welcome_channel_id = "C12345"
    user_id = event["user"]
    #dm_channel = message["channel"]
    text = f"Welcome to the team, <@{user_id}>! 🎉 You can introduce yourself in this channel."
    #say(text=text, channel=dm_channel)
    print(event)


def main():
    handler = SocketModeHandler(app, SOCKET_TOKEN_DEV)
    handler.start()


if __name__ == "__main__":
    main()



    #https://cse.taylor.edu/information/faq/
