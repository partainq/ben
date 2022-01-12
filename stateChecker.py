# dictofStates = {user_id: validState, etc}
dictofStates = {}
validStates = ['normal', 'triviaQuestion']

def checkState(user_id):
    if user_id not in dictofStates.keys():
        dictofStates[user_id] = 'normal'
    return dictofStates[user_id]

def changeState(user_id, newState):
    if newState in validStates:
        dictofStates[user_id] = newState
    return None
