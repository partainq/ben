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
import formats.weather, formats.help, formats.helpAll, formats.nextSemester, formats.chapel, formats.clubs, formats.laraHorsley, formats.abbreviations, formats.cseEvent

def commenceNormalState(message, say):
    dm_channel = message["channel"]
    user_id = message["user"]

    if compareValues(message['text'], "hey|hi|hello|howdy"):
        greeting = random.choice(["Hi there, ", "Hey, ", "Hello, ", "Great to hear from you, ", "Hi, "])
        msg = f"{greeting} <@{message['user']}>"

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

    elif compareValues(message['text'], "functions"):
        blocks = formats.helpAll.getFormat()
        say(blocks=blocks, text="helpAll", channel=dm_channel)

    elif compareValues(message['text'], 'add cse event'):
        say(text="Please enter admin password: ", channel=dm_channel)
        changeState(user_id, 'cseEvent')

    elif compareValues(message['text'], 'cse event'):
        tempCSEEvent = getNextCSEEvent()
        if ';' in tempCSEEvent:
            blocks = formats.cseEvent.getFormat(tempCSEEvent)
            say(blocks=blocks, text='CSE Event:',  channel=dm_channel)
        else:
            say(text=tempCSEEvent, channel=dm_channel)

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

    elif compareValues(message['text'], "club|clubs"):
        blocks = formats.clubs.getFormat()
        say(blocks=blocks, text="clubs", channel=dm_channel)

    elif compareValues(message['text'], "gamejam|game jam"):
        say(text="A *game jam* is a short, fun, and intense competition during which students get together to develop a video game from scratch. Regardless of major or knowledge of programming, all TU students are invited to participate! Find more information at https://gamejam.cse.taylor.edu/.", channel=dm_channel)
    
    elif compareValues(message['text'], "TWEET|tweet"):
        say(text="Taylor Women Engaged in Engineering and Technology, or TWEET, is a club that seeks to provide social, academic, and career development opportunities for women studying computer science and engineering (or both!). We seek to build community through events like TWEET Teas, Baking with Buddies, and game nights. \n\nInterested? Ask Lara Horsley for more information. Don't know who that is? Ask away!", channel=dm_channel)

    elif compareValues(message['text'], "Envisage|envisage"):
        say(text="Work in progress", channel=dm_channel)

    elif compareValues(message['text'], "TU Pilots|TUPILOTS|tu pilots"):
        say(text="TU Pilots is drone club on campus. The club welcomes people of all expierences. To learn more, ask Lara", channel=dm_channel)

    elif compareValues(message['text'], "Esports|esports"):
        say(text="Taylor Esports is an up-and-coming club on Taylor University’s campus! Its goal is to provide a central hub for all gamers on campus! Its aim is to have teams competing in every collegiate esport out there! Join the official Taylor Esports Discord to learn more at tayloresports.com.", channel=dm_channel)

    elif compareValues(message['text'], "Crossfit |TU XFIT|crossfit"):
        say(text="Taylor Crossfit offers the chance for a fitness regimen that involves constantly varied functional movements performed at high intensity. Ask the front desk at the KSAC for more information.", channel=dm_channel)

    elif compareValues(message['text'], "CCO|cco"):
        say(text="The Mission of the *Calling and Career Office* (CCO) is to connect students to people and experiences that guide them in discerning a faithful response to God’s call. Their office is located in the Student Center. They can help you write your resume or connect you with an internship!", channel=dm_channel)

    elif compareValues(message['text'], "counseling"):
        say(text="*Counseling Center*\n The stresses of academic life can be hard for anyone. Taylor has terrific counseling services available to help you navigate these issues.",channel=dm_channel)
        say(text="They are located on the second level of LaRita Boren Campus Center (right above Chick Fil A). You can email counselingcenter@taylor.edu or call 765-998-5222 to set up an appointment. Visit https://my.taylor.edu/counseling-center/ for an up-to-date overview of available services and contact information", channel=dm_channel)

    elif compareValues(message['text'], "tutor|tutoring"):
        say(text="*Tutoring Services*\n Peer Tutoring Services, located in the AEC in Zondervan Library, provides free help to students in most content areas. For further information, contact Darci Nurkkala, drnurkkala@taylor.edu. Additionally, you can text me *study table* and I can notify someone that a student anonymously requested one.",channel=dm_channel)
    
    elif compareValues(message['text'], "change major|major change|degree requirements|graduation"):
        say(text="*Major Changes and Degree Requirements*\n All information regarding changing your major, requirements, or graduation can be found in Euler 213. Ask Lara to point you in the right direction. Don't know who Lara is? Ask away!",channel=dm_channel)
    
    elif compareValues(message['text'], "special needs|scott barrett|aec|AEC|enrichment center"):
        say(text="*Academic Enrichment Center*\n The Academic Enrichment Center provides a variety of services for students who have disabilities. This includes, but is not limited to, mental, emotional, physical, and learning disabilities. Contact *Scott Barrett*, scott_barrett@taylor.edu, to learn more. If you need accommodations due to a disability, please also see your professor so that they can help accordingly.")

    elif compareValues(message['text'], "trivia"):
        changeState(user_id, 'trivia')
        commenceTriviaState(message,say)

    elif compareValues(message['text'], 'hangman'):
        changeState(user_id, 'hangman')
        commenceHangmanState(message,say)

    elif compareValues(message['text'], 'abbreviations'):
        blocks = formats.abbreviations.getFormat()
        say(blocks=blocks, text="abbreviations", channel=dm_channel)

    elif compareValues(message['text'], 'Lara|Horsley'):
        blocks = formats.laraHorsley.getFormat()
        say(blocks=blocks, text="Lara Horsley", channel=dm_channel)

    elif compareValues(message['text'], 'studytable|study table|table study'):
        changeState(user_id, 'studyTable')
        commenceStudyTableState(message,say)

    else:
        say(text="Not sure what you are saying...Code me further to do that! Text *help* to see what I can do.", channel=dm_channel)

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