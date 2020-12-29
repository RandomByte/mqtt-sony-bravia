import os
import time
import requests
import paho.mqtt.client as mqtt

tvIp = os.environ["MQTT_SB_TV_IP"]
mqttBrokerIp = os.environ["MQTT_SB_MQTT_BROKER"]
mqttTopicPrefix = os.environ["MQTT_SB_MQTT_TOPIC_PREFIX"]

pollInterval = 60; # every 1 minute
payload = {"id": 20, "method": "getCurrentExternalInputsStatus", "version": "1.0", "params": [""]}

mqttClient = mqtt.Client(client_id="mqtt-sony-bravia")
connected = False

knownInputs = set()

def onConnect(client, userdata, flags, rc):
	global connected
	connected = True

def onDisconnect(client, userdata, rc):
	global connected
	connected = False

def camelCase(s):
	s = s.title().replace(" ", "").replace("/", "")
	s = s[0].lower() + s[1:]
	return s

def poll():
	inputs=None
	try:
		r = requests.post(f"http://{tvIp}/sony/avContent", json = payload)
		res = r.json()
		if "error" in res:
			print(f"Poll failed with server error {res['error']}")
			return False
		inputs = res["result"][0]
	except requests.ConnectionError as e:
		print(f"Poll failed with connection error {e}")
		return False

	# Test data:
	#inputs = [{'connection': True, 'icon': 'meta:hdmi', 'label': '', 'title': 'HDMI 1', 'uri': 'extInput:hdmi?port=1'}, {'connection': False, 'icon': 'meta:hdmi', 'label': '', 'title': 'HDMI 2/MHL', 'uri': 'extInput:hdmi?port=2'}, {'connection': False, 'icon': 'meta:scart', 'label': '', 'title': 'AV1', 'uri': 'extInput:scart?port=1'}, {'connection': False, 'icon': 'meta:component', 'label': '', 'title': 'AV2/Component', 'uri': 'extInput:composite?port=1'}, {'connection': True, 'icon': 'meta:playbackdevice', 'label': 'PlayStation 4', 'title': 'Player 1', 'uri': 'extInput:cec?type=player&port=1'}, {'connection': True, 'icon': 'meta:playbackdevice', 'label': 'Apple TV', 'title': 'Player 2', 'uri': 'extInput:cec?type=player&port=2'}, {'connection': False, 'icon': 'meta:wifidisplay', 'label': '', 'title': 'Screen mirroring', 'uri': 'extInput:widi?port=1'}]
	print("Poll successful")
	for inputStatus in inputs:
		connStatus = "Disconnected"
		if inputStatus["connection"] == True:
			connStatus = "Connected"

		inputName = camelCase(inputStatus["title"])
		knownInputs.add(inputName)
		topic = mqttTopicPrefix + "Connections/" + inputName
		print(f"{topic} is {connStatus}")
		p = mqttClient.publish(topic, qos=1, payload=connStatus)
		p.wait_for_publish()

	return True

def handleFailedPoll():
	for inputName in knownInputs:
		connStatus = "Disconnected"
		topic = mqttTopicPrefix + "Connections/" + inputName
		print(f"Poll Failed: Updating {topic} as {connStatus}")
		p = mqttClient.publish(topic, qos=1, payload=connStatus)
		p.wait_for_publish()


if __name__ == "__main__":
	lastPoll = 0
	lastPollFailed = False
	mqttClient.on_connect = onConnect
	mqttClient.on_disconnect = onDisconnect
	mqttClient.connect(mqttBrokerIp, 1883, 60)
	mqttClient.loop_start()

	while True:
		currTs = time.time()
		if connected and currTs - lastPoll > pollInterval:
			lastPoll = currTs
			print("Polling...")
			success = poll()
			if success:
				lastPollFailed = False
			elif lastPollFailed == False:
				handleFailedPoll()
				lastPollFailed = True
