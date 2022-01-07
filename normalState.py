from app import *

triviaList = [("do birds have heads?", "yes"), ("is Snape evil?", "no"), ("please stop", "no"), ("how about now", "no")]

def commenceNormalState(payload):
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
        message = "The result is " + results

        client.chat_postMessage(channel=channel_id, text=message)

    elif user_id != BOT_ID and "weather" in text.lower():
        weather_key = "32843bad9e96bb36c7935458544b1628"
        lat = "48.208176"
        lon = "16.373819"
        url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (
        lat, lon, weather_key)
        # response = requests.get(url)
        # data = json.loads(response.text)
        client.chat_postMessage(channel=channel_id, text="weather")

    elif user_id != BOT_ID and 'game' in text.lower():
        client.chat_postMessage(channel=channel_id, text="Did someone say game!")
        client.chat_postMessage(channel=channel_id, text="I love games!!")
        client.chat_postMessage(channel=channel_id, text="Lets play trivia")
        tempQuestion = random.choice(triviaList)
        client.chat_postMessage(channel=channel_id, text=tempQuestion[0])
        changeState(channel_id, 'triviaQuestionState')
        triviaAnswer(channel_id, tempQuestion[1])

    elif user_id != BOT_ID:
        client.chat_postMessage(channel=channel_id, text=text)