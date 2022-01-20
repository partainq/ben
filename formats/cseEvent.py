
def getFormat(cseEvent):
    newCSEEvent = cseEvent.split(';')
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Name:* " + newCSEEvent[0] +"\n *Date:* " + newCSEEvent[1] +"\n *Note:* " + newCSEEvent[2]
            },
        },
    ]