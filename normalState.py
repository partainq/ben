from bolt_socket import *

triviaList = [("do birds have heads?", "yes"), ("is Snape evil?", "no"), ("please stop", "no"), ("how about now", "no")]


def commenceNormalState(message, say):
    # event = payload.get('event', {})
    # channel_id = event.get('channel')
    # user_id = event.get('user')
    # text = event.get('text')
    channel_type = message["channel_type"]
    dm_channel = message["channel"]
    user_id = message["user"]
    name = app.client.users_info(user=user_id)["user"]["name"]

    if message['text'][-1] == "=":
        numbers = message['text'].split()
        if numbers[1] == "-":
            say(text=int(numbers[0]) - int(numbers[2], channel=dm_channel))
        if numbers[1] == "*":
            say(text=int(numbers[0]) * int(numbers[2], channel=dm_channel))
        if numbers[1] == "+":
            say(text=int(numbers[0]) + int(numbers[2], channel=dm_channel))

    elif message['text'] =="how are you" or message['text']=="how is your day|how was your day|how are ya":
        message = random.choice(["Having another day to help people is a blessing.",
                                 "Looks like my server is still up, so it is a good day!",
                                 "It's a great day to have a great day!", "Wonderful!"])
        say(text=message, channel=dm_channel)

    elif message['text'] == "whats up" or message['text']=="|what up|what's up|sup":
        message = random.choice(["Not much. Life is pretty quiet as a chatbot.",
                                 "Some movie about an old guy, balloons, and a flying house",
                                 "What can I help you with today?", "Great to hear from you."])

        say(text=message, channel=dm_channel)

    elif message['text'] == "joke":
        joke = pyjokes.get_joke()
        say(text=joke, channel=dm_channel)

    elif message['text'] == "what are you" or message['text']=="|who are you|do you do|help|can you do|purpose|capabilities":
        blocks = formats.help.getFormat()

        say(blocks=blocks, text="hi", channel=dm_channel)

    elif message['text'] == "flip a coin":
        rand_int = random.randint(0, 1)
        if rand_int == 0:
            results = "Coin Flip: heads"
        else:
            results = "Coin Flip: tails"

        say(text=results, channel=dm_channel)

    elif message['text'] == "weather":
        lat = "40"
        lon = "-85"

        url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=imperial" % (
        lat, lon, WEATHER_KEY)
        request = json.loads(requests.get(url).text)["current"]

        icon = request["weather"][0]['icon']
        temp = request["temp"]
        description = request["weather"][0]["main"]

        print(request)
        blocks = formats.weather.getFormat(temp, icon, description)

        say(blocks=blocks, text="weather", channel=dm_channel)

    # elif message == "next semester" or message=="|next term|classes next|next classes|next year":
    #     url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=imperial" % (
    #     lat, lon, WEATHER_KEY)
    #     request = json.loads(requests.get(url).text)["current"]
    #
    #     icon = request["weather"][0]['icon']
    #     temp = request["temp"]
    #     description = request["weather"][0]["main"]
    #     dm_channel = message["channel"]
    #
    #     print(request)
    #     blocks = formats.weather.getFormat(temp, icon, description)
    #
    #     say(blocks=blocks, text="weather", channel=dm_channel)

