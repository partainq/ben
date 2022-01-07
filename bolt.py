#trying something new..
import logging
import os
import re
import random
import requests, json

import formats.weather

from dotenv import load_dotenv
import pyjokes
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# gooda = xapp-1-A02SQ341ZCL-2926074915076-9b5c250da6ad7ec38d1ee832aca98e18acde5f0eebd3864d3abe8b540aa35854


load_dotenv()

SOCKET_TOKEN_DEV = os.environ["SOCKET_TOKEN_DEV"]
SLACK_TOKEN_DEV = os.environ["SLACK_TOKEN_DEV"]
WEATHER_KEY = os.environ["WEATHER_KEY"]

app = App(token=SLACK_TOKEN_DEV, name="ben")
logger = logging.getLogger(__name__)


@app.message(re.compile("joke"))  # type: ignore
def random_joke(message, say):
    channel_type = message["channel_type"]
    #if channel_type != "im": #im = direct channel
    #    return

    dm_channel = message["channel"]
    user_id = message["user"]

    joke = pyjokes.get_joke()
    say(text=joke, channel=dm_channel)

@app.message(re.compile("flip a coin" or "coin flip"))
def coin_flip(message, say):
    channel_type = message["channel_type"]
    #if channel_type != "im":
    #    return
    
    dm_channel = message["channel"]
    rand_int = random.randint(0, 1)
    if rand_int == 0:
        results = "Coin Flip: heads"
    else:
        results = "Coin Flip: tails"

    say(text=results, channel=dm_channel)

@app.message(re.compile("weather"))
def weather(message, say):
    channel_type = message["channel_type"]
    #if channel_type != "im":
    #    return
    
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

    say(blocks=blocks, text="hi", channel=dm_channel)

def main():
    handler = SocketModeHandler(app, SOCKET_TOKEN_DEV)
    handler.start()


if __name__ == "__main__":
    main()