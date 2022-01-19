def getFormat(reason):
    formattedReason = "*Reason:*\n"+reason
    return [
        {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Hey there 👋 . I have a system that lets students request the need for a study table. Below is an anonymous request. Thank you for all you do! \n\n"
			}
		},
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*Study Table Alert:*\nA student has anonmously notified me that there is a need for a study table."
                },
                {
                    "type": "mrkdwn",
                    "text": formattedReason
                },
            ]
		}
	]