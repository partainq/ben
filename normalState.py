from bolt_socket import *
from datetime import date, datetime
from stateChecker import *
from triviaState import *
from helpfulFunctions import *
from hangmanState import *


load_dotenv()



def commenceNormalState(message, say):
    # event = payload.get('event', {})
    # channel_id = event.get('channel')
    # user_id = event.get('user')
    # text = event.get('text')
    channel_type = message["channel_type"]
    dm_channel = message["channel"]
    user_id = message["user"]

    if message['text'][-1] == "=":
        numbers = message['text'].split()
        if numbers[1] == "-":
            say(text=int(numbers[0]) - int(numbers[2], channel=dm_channel))
        if numbers[1] == "*":
            say(text=int(numbers[0]) * int(numbers[2], channel=dm_channel))
        if numbers[1] == "+":
            say(text=int(numbers[0]) + int(numbers[2], channel=dm_channel))
    
    elif compareValues(message['text'], "hi"):
        greeting = random.choice(["Hi there, ", "Hey, ", "Hello, ", "Great to hear from you, ", "Hi, "])
        msg = f"{greeting} <@{message['user']}>"

        say(text=msg, channel=dm_channel)

    elif compareValues(message['text'], "how are you|how is your day|how was your day|how are ya"):
        message = random.choice(["Having another day to help people is a blessing.",
                                 "Looks like my server is still up, so it is a good day!",
                                 "It's a great day to have a great day!", "Wonderful!"])

        say(text=message, channel=dm_channel)

    elif compareValues(message['text'], "whats up|what up|what's up|sup"):
        message = random.choice(["Not much. Life is pretty quiet as a chatbot.",
                                 "Some movie about an old guy, balloons, and a flying house",
                                 "What can I help you with today?", "Great to hear from you."])

        say(text=message, channel=dm_channel)

    elif compareValues(message['text'], "joke"):
        say(text=pyjokes.get_joke(), channel=dm_channel)

    elif compareValues(message['text'], "what are you|who are you|do you do|help|can you do|purpose|capabilities"):
        blocks = formats.help.getFormat()

        say(blocks=blocks, text="help", channel=dm_channel)

    elif compareValues(message['text'], "flip a coin"):
        rand_int = random.randint(0, 1)
        if rand_int == 0:
            results = "Coin Flip: heads"
        else:
            results = "Coin Flip: tails"

        say(text=results, channel=dm_channel)

    elif compareValues(message['text'], "weather"):
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
    
    elif compareValues(message['text'], "next semester|next term|classes next|next classes|next year"):
        term_id = getTermId()
        url = "http://api.dev.envisageplanner.com/courses/term-sections/" + str(term_id)

        request = json.loads(requests.get(url).text)

        classes = []
        for x in range(len(request)):
            if request[x]["Course"]["idProvided"][0:3] == "COS":
                classes.append(request[x]["Course"])

        blocks = formats.nextSemester.getFormat(classes, getNextTerm())

        say(blocks=blocks, text="next semester", channel=dm_channel)

    elif compareValues(message['text'], "trivia|lets play trivia|I like trivia"):
        changeState(user_id, 'trivia')
        commenceTriviaState(message,say)

    elif compareValues(message['text'], 'hangman'):
        changeState(user_id, 'hangman')
        commenceHangmanState(message,say)


    else:
        say(text="Not sure what you are saying...Code me further to do that!", channel=dm_channel)


def getTermId():
    url = "https://api.dev.envisageplanner.com/terms"
    request = json.loads(requests.get(url).text)
    currentTerm = getNextTerm()

    for x in request:
        if x["name"] == currentTerm:
            return x["id"]

    return "0"

def getNextTerm():
    doy = datetime.today().timetuple().tm_yday
    currentYear = datetime.now().year

    spring = range(33, 152)
    summer = range(152, 234)
    fall = range(234, 348)

    if doy in spring:
        season = 'Summer'
    elif doy in summer:
        season = 'Fall'
    elif doy in fall:
        season = 'Interem'
    else:
        season = 'Spring'

    return season + " " + str(currentYear)

