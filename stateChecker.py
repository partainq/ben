
# dictofStates = {channel_id: validState, etc}
dictofStates = {}
validStates = ['normal', 'triviaQuestion']

def checkState(channel_id):
    if channel_id not in dictofStates.keys():
        dictofStates[channel_id] = 'normal'
    return dictofStates[channel_id]

def changeState(channel_id, newState):
    if newState in validStates:
        dictofStates[channel_id] = newState
    return None
