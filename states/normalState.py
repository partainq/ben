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

    if compareValues(message['text'].lower(), "hey|hello |howdy "):
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

    elif compareValues(message['text'].lower(), "how are you|how is your day|how was your day|how are ya"):
        message = random.choice(["Having another day to help people is a blessing.",
                                 "Looks like my server is still up, so it is a good day!",
                                 "It's a great day to have a great day!", "Wonderful!"])

        say(text=message, channel=dm_channel)

    elif compareValues(message['text'].lower(), "whats up|what up|what's up|sup"):
        message = random.choice(["Not much. Life is pretty quiet as a chatbot.",
                                 "Just enjoying life",
                                 "What can I help you with today?", "Great to hear from you."])

        say(text=message, channel=dm_channel)

    elif compareValues(message['text'].lower(), "joke"):
        say(text=pyjokes.get_joke(), channel=dm_channel)

    elif compareValues(message['text'].lower(), "what are you|who are you|do you do|help|can you do|purpose|capabilities"):
        blocks = formats.help.getFormat()
        say(blocks=blocks, text="help", channel=dm_channel)

    elif compareValues(message['text'].lower(), "functions"):
        blocks = formats.helpAll.getFormat()
        say(blocks=blocks, text="helpAll", channel=dm_channel)

    elif compareValues(message['text'].lower(), 'add cse event'):
        say(text="Please enter admin password: ", channel=dm_channel)
        changeState(user_id, 'cseEvent')

    elif compareValues(message['text'].lower(), 'cse event'):
        tempCSEEvent = getNextCSEEvent()
        if ';' in tempCSEEvent:
            blocks = formats.cseEvent.getFormat(tempCSEEvent)
            say(blocks=blocks, text='CSE Event:',  channel=dm_channel)
        else:
            say(text=tempCSEEvent, channel=dm_channel)

    elif compareValues(message['text'].lower(), "flip a coin"):
        rand_int = random.randint(0, 1)
        if rand_int == 0:
            results = "Coin Flip: heads"
        else:
            results = "Coin Flip: tails"

        say(text=results, channel=dm_channel)

    elif compareValues(message['text'].lower(), "weather"):
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
    
    elif compareValues(message['text'].lower(), "next semester|next term|classes next|next classes|next year"):
        term_id = getTermId()
        url = "http://api.dev.envisageplanner.com/courses/term-sections/" + str(term_id)

        request = json.loads(requests.get(url).text)

        classes = []
        for x in range(len(request)):
            if request[x]["Course"]["idProvided"][0:3] == "COS":
                classes.append(request[x]["Course"])

        blocks = formats.nextSemester.getFormat(classes, getNextTerm())

        say(blocks=blocks, text="next semester", channel=dm_channel)

    elif compareValues(message['text'].lower(), "chapel"):
        blocks = formats.chapel.getFormat()
        say(blocks=blocks, text="next semester", channel=dm_channel)

    elif compareValues(message['text'].lower(), "club|clubs"):
        blocks = formats.clubs.getFormat()
        say(blocks=blocks, text="clubs", channel=dm_channel)

    elif compareValues(message['text'].lower(), "gamejam|game jam"):
        say(text="A *game jam* is a short, fun, and intense competition during which students get together to develop a video game from scratch. Regardless of major or knowledge of programming, all TU students are invited to participate! Find more information at https://gamejam.cse.taylor.edu/.", channel=dm_channel)
    
    elif compareValues(message['text'].lower(), "tweet"):
        say(text="Taylor Women Engaged in Engineering and Technology, or TWEET, is a club that seeks to provide social, academic, and career development opportunities for women studying computer science and engineering (or both!). We seek to build community through events like TWEET Teas, Baking with Buddies, and game nights. \n\nInterested? Ask Lara Horsley for more information. Don't know who that is? Ask away!", channel=dm_channel)

    elif compareValues(message['text'].lower(), "envisage"):
        say(text="Envisage planner is an intuitive tool built by and for TU students to help you with the process of choosing your major/minor, courses, and when and how to take them. Anyone with an @taylor.edu address can sign up for free! Learn more at their website: *envisageplanner.com*", channel=dm_channel)

    elif compareValues(message['text'].lower(), "tupilots|tu pilots"):
        say(text="TU Pilots is a drone club on campus. The club welcomes people of all expierences. To learn more, ask Lara", channel=dm_channel)

    elif compareValues(message['text'].lower(), "esports"):
        say(text="Taylor Esports is an up-and-coming club on Taylor University’s campus! Its goal is to provide a central hub for all gamers on campus! Its aim is to have teams competing in every collegiate esport out there! Join the official Taylor Esports Discord to learn more at tayloresports.com.", channel=dm_channel)

    elif compareValues(message['text'].lower(), "tu xfit|crossfit"):
        say(text="Taylor Crossfit offers the chance for a fitness regimen that involves constantly varied functional movements performed at high intensity. Ask the front desk at the KSAC for more information.", channel=dm_channel)

    elif compareValues(message['text'].lower(), "cco|calling and career"):
        say(text="The Mission of the *Calling and Career Office* (CCO) is to connect students to people and experiences that guide them in discerning a faithful response to God’s call. Their office is located in the Student Center. They can help you write your resume or connect you with an internship!", channel=dm_channel)

    elif compareValues(message['text'].lower(), "counseling"):
        say(text="*Counseling Center*\n The stresses of academic life can be hard for anyone. Taylor has terrific counseling services available to help you navigate these issues.",channel=dm_channel)
        say(text="They are located on the second level of LaRita Boren Campus Center (right above Chick Fil A). You can email counselingcenter@taylor.edu or call 765-998-5222 to set up an appointment. Visit https://my.taylor.edu/counseling-center/ for an up-to-date overview of available services and contact information", channel=dm_channel)

    elif compareValues(message['text'].lower(), "tutor|tutoring"):
        say(text="*Tutoring Services*\n Peer Tutoring Services, located in the AEC in Zondervan Library, provides free help to students in most content areas. For further information, contact Darci Nurkkala, drnurkkala@taylor.edu. Additionally, you can text me *study table* and I can notify someone that a student anonymously requested one.",channel=dm_channel)
    
    elif compareValues(message['text'].lower(), "change major|major change|degree requirements|graduation"):
        say(text="*Major Changes and Degree Requirements*\n All information regarding changing your major, requirements, or graduation can be found in Euler 213. Ask Lara to point you in the right direction. Don't know who Lara is? Ask away!",channel=dm_channel)
    
    elif compareValues(message['text'].lower(), "special needs|scott barrett|aec|enrichment center"):
        say(text="*Academic Enrichment Center*\n The Academic Enrichment Center provides a variety of services for students who have disabilities. This includes, but is not limited to, mental, emotional, physical, and learning disabilities. Contact *Scott Barrett*, scott_barrett@taylor.edu, to learn more. If you need accommodations due to a disability, please also see your professor so that they can help accordingly.")

    elif compareValues(message['text'].lower(), "trivia"):
        changeState(user_id, 'trivia')
        commenceTriviaState(message,say)

    elif compareValues(message['text'].lower(), 'hangman'):
        changeState(user_id, 'hangman')
        commenceHangmanState(message,say)

    elif compareValues(message['text'].lower(), 'studytable|study table|homework'):
        changeState(user_id, 'studyTable')
        commenceStudyTableState(message,say)

    elif compareValues(message['text'].lower(), 'abbreviations'):
        blocks = formats.abbreviations.getFormat()
        say(blocks=blocks, text="abbreviations", channel=dm_channel)

    elif compareValues(message['text'].lower(), 'lara|horsley'):
        blocks = formats.laraHorsley.getFormat()
        say(blocks=blocks, text="Lara Horsley", channel=dm_channel)

    elif compareValues(message['text'].lower(), 'i love you'):
        say(text="I love you too....I think.", channel=dm_channel)

    elif compareValues(message['text'].lower(), "color"):
        say(text="My *favorite color* system tells me that I like *100000000000000010000000*, but I can't remember how to decode it. Can you?", channel=dm_channel)

    elif compareValues(message['text'].lower(), 'quinn|micah'):
        say(text="*Quinn Partain* and *Micah Odell* are the people who made me possible.", channel=dm_channel)

    elif compareValues(message['text'].lower(), 'thank you | thankyou | thanks'):
        msg = random.choice(["You are welcome!",
                            "You are so welcome. Thank you for saying thank you.😄 "])   
        say(text=msg, channel=dm_channel)

    elif compareValues(message['text'].lower(), 'favorite class'):
        say(text="My *favorite class* was COS243, Multi-tier Web Application Development. That was a great class and I learned alot, useful for internships, and I had fun. Interested in seeing if it is offered next year? Text *next semester* to see if it is offered. ", channel=dm_channel)

    elif compareValues(message['text'].lower(), 'hardest class'):
        say(text="The *hardest class* I ever took was Machine Learning. It was a lot of work, but very applicable and helpful.", channel=dm_channel)

    elif compareValues(message['text'].lower(), 'internship'):
        say(text="If you are looking for an *internship*, the best thing you can do is talk to alumni. Alumni love connecting you with Taylor Students. Not sure of any alumni? Talk to Lara or a professor to help you out! It is never too early to get an internship.", channel=dm_channel)

    elif compareValues(message['text'].lower(), 'ide'):
        say(text="Visual Studio Code is the way to go.😎", channel=dm_channel)
    
    elif compareValues(message['text'].lower(), 'videogame|videogames|video games'):
        say(text="My favorite *videogame* is Old School Runescape. If you like video games, check out the Taylor Esports club! Learn more by texting *esports*. ", channel=dm_channel)

    elif compareValues(message['text'].lower(), "hi"):
        greeting = random.choice(["Hi there, ", "Hello, "])
        msg = f"{greeting} <@{message['user']}>."

        say(text=msg, channel=dm_channel)

    elif message['text'] == "Do I look fat?":
        say(text="No, you look perfect!", channel=dm_channel)

    elif compareValues(message['text'].lower(), "Would this girl go out with me"):
        say(text="Any girl would be lucky to go out with you!! :)", channel=dm_channel)

    elif compareValues(message['text'].lower(), "Would this guy go out with me"):
        say(text="Any guy would be lucky to go out with you!! :)", channel=dm_channel)

    elif compareValues(message['text'].lower(), "Who is the best basketball player ever?"):
        say(text='Mike Miller', channel=dm_channel)

    elif compareValues(message['text'].lower(), "What is the best movie series of all time?"):
        say(text='Lord of the Rings', channel=dm_channel)

    elif compareValues(message['text'].lower(), "Who is the best League of Legends character?"):
        say(text="Teemo", channel=dm_channel)

    elif compareValues(message['text'].lower(), "Teemo"):
        say(text="Never underestimate the power of the scouts code!", channel=dm_channel)

    elif compareValues(message['text'].lower(), "Whats the number 2 donut shop in the country?"):
        say(text="Bill's Donut Shop", channel=dm_channel)

    elif compareValues(message['text'].lower(), "Crypto?"):
        say(text="That stuff is over my head, however I'm sure a legendary Dr. Geisler would love to help!", channel=dm_channel)

    elif compareValues(message['text'].lower(), "Best pirate ever?"):
        say(text="Captain Jack Sparrow", channel=dm_channel)

    elif compareValues(message['text'].lower(), "Should we go to Dans?"):
        say(text="Yes!! I love donuts!", channel=dm_channel)

    elif compareValues(message['text'].lower(), "Who is the best League of Legends character?"):
        say(text="Teemo", channel=dm_channel)

    elif compareValues(message['text'].lower(), "Is Trevor fat?"):
        say(text="From my angle he's huge!", channel=dm_channel)

    else:
        print(message['text'])
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