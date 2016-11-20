
import paho.mqtt.client as mqtt

MQTT_ADDRESS = '192.168.0.48'
MQTT_PORT = 1883

MQTT_ID = 'FritzScraper'

class MqttConnection(object):

  def __init__(self, address=MQTT_ADDRESS, port=MQTT_PORT):
    self.address = address
    self.port = port
    self.connected = False

    self.client = mqtt.Client(MQTT_ID)
    self.client.on_connect = self.mqtt_on_connect
    self.client.on_disconnect = self.mqtt_on_disconnect

  def mqtt_on_connect(self, client, userdata, flags, rc):
    connack_string = {0:'Connection successful',
                      1:'Connection refused - incorrect protocol version',
                      2:'Connection refused - invalid client identifier',
                      3:'Connection refused - server unavailable',
                      4:'Connection refused - bad username or password',
                      5:'Connection refused - not authorised'}

    if rc:
      print(connack_string[rc])
    else:
      print("Connection status: "+connack_string[rc])
      self.connected = True

  def mqtt_on_disconnect(self, client, userdata, rc):
    if rc != 0:
      print("Unexpected disconnection")
      self.connected = False

  def connect(self):
    if not self.connected:
      print("Connecting to MQTT Broker.")
      try:
        self.client.username_pw_set("emoncms", "FNnB6Qnr6Mgt7h2hYROA")
        self.client.connect(self.address, self.port, 60)
      except:
        print("Error connecting...")
        time.sleep(1)
    self.client.loop(0)

  def disconnect(self):
    self.client.disconnect()

  def publish(self, cargo):
    if self.connected:

      varid = 1
      for value in cargo.values:

        # Get name of variable
        varstr = str(cargo.names[varid-1])

        # Construct topic
        topic = BASE_TOPIC + '/' + varstr
        payload = str(value)

        print("Publishing: " + topic + " " + payload)
        result = self.client.publish(topic, payload=payload, qos=2, retain=False)

        if result[0] == 4:
          print("Publishing error")

        varid += 1
