
import paho.mqtt.client as mqtt

MQTT_ADDRESS = '192.168.0.48'
MQTT_PORT = 1883

MQTT_ID = 'FritzScraper'

BASE_TOPIC = 'fritzscraper/fritz_1'

class MqttConnection(object):

  _client = None
  _address = MQTT_ADDRESS
  _port = MQTT_PORT
  _connected = False

  def __init__(self, address=MQTT_ADDRESS, port=MQTT_PORT):
    self._address = address
    self._port = port
    self._connected = False

    self._client = mqtt.Client(MQTT_ID)
    self._client.on_connect = self.on_connect
    self._client.on_disconnect = self.on_disconnect

  def on_connect(self, client, userdata, flags, rc):
    connack_string = {0:'Connection successful',
                      1:'Connection refused - incorrect protocol version',
                      2:'Connection refused - invalid client identifier',
                      3:'Connection refused - server unavailable',
                      4:'Connection refused - bad username or password',
                      5:'Connection refused - not authorised'}

    if rc:
      print(connack_string[rc])
    else:
      print("Connection status: " + connack_string[rc])
      self._connected = True

  def on_disconnect(self, client, userdata, rc):
    if rc != 0:
      print("Unexpected disconnection")
    print("Disconnected from MQTT Broker.")
    self._connected = False
    self._client.loop_stop()

  def connect(self):
    if not self._connected:
      print("Connecting to MQTT Broker.")
      try:
        self._client.username_pw_set("emoncms", "FNnB6Qnr6Mgt7h2hYROA")
        self._client.connect(self._address, self._port, 60)
        self._client.loop_start()
      except:
        print("Error connecting...")
        self._client.loop_stop()

  def disconnect(self):
    self._client.loop_stop()
    self._client.disconnect()

  def publish(self, fscargo):
    if self._connected:
      for name, value in fscargo.cargo.items():

        # Construct topic
        topic = BASE_TOPIC + '/' + str(name)
        payload = str(value)

        print("Publishing: " + topic + " " + payload)
        #result = self._client.publish(topic, payload=payload, qos=2, retain=False)
        result = 4

        if result == 4:
          print("Publishing error")
