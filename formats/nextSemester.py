def getFormat(classes, term):
    block = [
        {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "COS classes offered *" + term +"*"
			}
		},
		{
			"type": "divider"
		},
    ]
    block.append(
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": ""
			}
		})

    for x in range(len(classes)):
        block[2]["text"]["text"] += "*"+classes[x]["idProvided"] + "*: " + classes[x]["name"] + "\n"
	
    block.append(
		{
			"type": "divider"
		},
	)
    block.append(
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "<https://cse.taylor.edu/information/info/|More information available here>"
			}
		}
	)
    
    return block