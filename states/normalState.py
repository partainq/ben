from app import *
from datetime import date, datetime
from helpers.stateChecker import *
from states.triviaState import *
from helpers.compare import *
from states.hangmanState import *
from states.studyTableState import *
from states.cseEventState import getNextCSEEvent

import random
import pyjokes
import requests, json
import formats.weather, formats.help, formats.nextSemester, formats.chapel, formats.clubs, formats.laraHorsley

load_dotenv()

def commenceNormalState(message, say):
    dm_channel = message["channel"]
    user_id = message["user"]

    
    if compareValues(message['text'], "hey|hi|hello|howdy"):
        greeting = random.choice(["Hi there, ", "Hey, ", "Hello, ", "Great to hear from you, ", "Hi, "])
        msg = f"{greeting} <@{message['user']}>"

        # print(dm_channel)
        say(text=msg, channel=dm_channel)

    elif message['text'][-1] == "=":
        numbers = message['text'].split()
        if numbers[1] == "-":
            say(text=str(int(numbers[0]) - int(numbers[2])), channel=dm_channel)
        if numbers[1] == "*":
            say(text=str(int(numbers[0]) * int(numbers[2])), channel=dm_channel)
        if numbers[1] == "+":
            say(text=str(int(numbers[0]) + int(numbers[2])), channel=dm_channel)

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

    elif compareValues(message['text'], 'add cse event'):
        say(text="Please enter admin password: ", channel=dm_channel)
        changeState(user_id, 'cseEvent')

    elif compareValues(message['text'], 'cse event'):
        say(text=getNextCSEEvent(), channel=dm_channel)

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

    elif compareValues(message['text'], "chapel"):
        blocks = formats.chapel.getFormat()
        say(blocks=blocks, text="next semester", channel=dm_channel)

    elif compareValues(message['text'], "club"):
        blocks = formats.clubs.getFormat()
        say(blocks=blocks, text="clubs", channel=dm_channel)

    elif compareValues(message['text'], "gamejam|game jam"):
        say(text="A *game jam* is a short, fun, and intense competition during which students get together to develop a video game from scratch. Regardless of major or knowledge of programming, all TU students are invited to participate! Find more information at https://gamejam.cse.taylor.edu/.", channel=dm_channel)
    
    elif compareValues(message['text'], "TWEET"):
        say(text="Taylor Women Engaged in Engineering and Technology, or TWEET, is a club that seeks to provide social, academic, and career development opportunities for women studying computer science and engineering (or both!). We seek to build community through events like TWEET Teas, Baking with Buddies, and game nights. \n\nInterested? Ask Lara Horsley for more information. Don't know who that is? Ask away!", channel=dm_channel)

    elif compareValues(message['text'], "Envisage"):
        say(text="Work in progress", channel=dm_channel)

    elif compareValues(message['text'], "TU Pilots|TUPILOTS"):
        say(text="Work in progress", channel=dm_channel)

    elif compareValues(message['text'], "Esports"):
        say(text="Taylor Esports is an up-and-coming club on Taylor University’s campus! Our goal is to provide a central hub for all gamers on campus! We aim to have teams competing every collegiate esport out there! Join the official Taylor Esports Discord to learn more at tayloresports.com.", channel=dm_channel)

    elif compareValues(message['text'], "Crossfit |TU XFIT"):
        say(text="Work in progress", channel=dm_channel)
    
    elif compareValues(message['text'], "trivia|lets play trivia|I like trivia"):
        changeState(user_id, 'trivia')
        commenceTriviaState(message,say)

    elif compareValues(message['text'], 'hangman'):
        changeState(user_id, 'hangman')
        commenceHangmanState(message,say)

    elif compareValues(message['text'], 'abbreviations'):
        abbreviations = "DTR = Define the relationship\nSTU = Student Center\nDC = Dining Commons\nTWO = Taylor World Outreach\nKSAC = Keisler Student Activity Center\nTSO = Taylor Student Organization\nSAC = Student Activity Council"
        say(text=abbreviations, channel=dm_channel)

    elif compareValues(message['text'], 'Lara|Horsley'):
        blocks = formats.laraHorsley.getFormat()
        say(blocks=blocks, text="Lara Horsley", channel=dm_channel)

    elif compareValues(message['text'], 'studytable|study table|table study'):
        changeState(user_id, 'studyTable')
        commenceStudyTableState(message,say)

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