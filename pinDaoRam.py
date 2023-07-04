import json

pin_conf_file = open('./pin_config.json')
pin_conf = json.loads(pin_conf_file.read())

def getPins():
	data = {}
	for i in range(1, pin_conf['pinNumber'] + 1):
		iStr = str(i)
		data["pin" + iStr] = {
			"name": iStr,
			"enabled": pin_conf[iStr],
			"mode": "-",
			"value": "-"
		}
	return data
	
