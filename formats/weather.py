def getFormat(temp, icon, description):
    return [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Taylor University Weather*\nTemperature: "+str(temp)+"\n"+description+"\n\nIt's going to be a great day :)"
			},
			"accessory": {
				"type": "image",
				"image_url": "http://openweathermap.org/img/wn/"+icon+".png",
                "alt_text": "image"
			},
		},
	]