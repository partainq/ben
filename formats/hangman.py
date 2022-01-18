
def getFormat(lives, word):
	if lives == 5:
		return [
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": word + "                                 ❤❤❤❤❤"
				},
			},
		]
	elif lives == 4:
		return [
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": word + "                                 ❤❤❤❤💔"
				},
			},
		]
	elif lives == 3:
		return [
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": word + "                                 ❤❤❤💔💔"
				},
			},
		]
	elif lives == 2:
		return [
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": word + "                                 ❤❤💔💔💔"
				},
			},
		]
	elif lives == 1:
		return [
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": word + "                                 ❤💔💔💔💔"
				},
			},
		]
	elif lives == 0:
		return [
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": word + "                                 💔💔💔💔💔"
				},
			},
		]

