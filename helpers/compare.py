import Levenshtein

def compareValues(msg, correctAnswer):
    correctAnswers = correctAnswer.split('|')
    for x in correctAnswers:
        if Levenshtein.distance(x, msg) <= (len(msg)//3):
            return True
        elif x in msg:
            return True
    return False