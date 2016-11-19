#!/usr/bin/env python

import paho.mqtt.client as mqtt
import fritzconnection as fc

import time

FRITZ_IP_ADDRESS = '192.168.0.1'
FRITZ_TCP_PORT = 49000

MQTT_ADDRESS = '192.168.0.48'
MQTT_PORT = 1883

MQTT_ID = 'FritzScraper'

class FritzScraperCargo(object):
  timestamp = 0.0
  names = []
  values = []

  def __init__(self, timestamp, names, values):
    self.timestamp = float(timestamp)
    self.names = names
    self.values = values


class FritzScraper(object):

  def __init__(self, address=FRITZ_IP_ADDRESS, port=FRITZ_TCP_PORT):
    connection = fc.FritzConnection(address=address, port=port)
    print("Connected to FritzBox")

    self.connection = connection
    self.last_bytes_sent = self.bytes_sent 
    self.last_bytes_received = self.bytes_received
    self.last_traffic_call = time.time()

  @property
  def modelname(self):
    return self.connection.modelname

  @property
  def is_linked(self):
    status = self.connection.call_action('WANCommonInterfaceConfig', 'GetCommonLinkProperties')
    return status['NewPhysicalLinkStatus'] == 'Up'

  @property
  def is_connected(self):
    status = self.connection.call_action('WANIPConnection', 'GetStatusInfo')
    return status['NewConnectionStatus'] == 'Connected'

  @property
  def wan_access_type(self):
    return self.connection.call_action('WANCommonInterfaceConfig', 'GetCommonLinkProperties')['NewWANAccessType']

  @property
  def external_ip(self):
    return self.connection.call_action('WANIPConnection', 'GetExternalIPAddress')['NewExternalIPAddress']

  @property
  def uptime(self):
    return self.connection.call_action('WANIPConnection', 'GetStatusInfo')['NewUptime']

  @property
  def bytes_received(self):
    return self.connection.call_action('WANCommonInterfaceConfig', 'GetTotalBytesReceived')['NewTotalBytesReceived']

  @property
  def bytes_sent(self):
    return self.connection.call_action('WANCommonInterfaceConfig', 'GetTotalBytesSent')['NewTotalBytesSent']

  @property
  def transmission_rate(self):
    sent = self.bytes_sent
    received = self.bytes_received
    traffic_call = time.time()
    time_delta = traffic_call - self.last_traffic_call
    upstream = int(1.0 * (sent - self.last_bytes_sent)/time_delta)
    downstream = int(1.0 * (received - self.last_bytes_received)/time_delta)
    self.last_bytes_sent = sent
    self.last_bytes_received = received
    self.last_traffic_call = traffic_call
    return upstream, downstream

  @property
  def max_bit_rate(self):
    status = self.connection.call_action('WANCommonInterfaceConfig', 'GetCommonLinkProperties')
    downstream = status['NewLayer1DownstreamMaxBitRate']
    upstream = status['NewLayer1UpstreamMaxBitRate']
    return upstream, downstream

  @property
  def max_byte_rate(self):
    upstream, downstream = self.max_bit_rate
    return upstream / 8.0, downstream / 8.0

  def print_status(self):
    print('model: ' + scraper.modelname)
    print('linked: ' + str(scraper.is_linked))
    print('connected: ' + str(scraper.is_connected))
    print('wan access: ' + scraper.wan_access_type)
    print('external ip: ' + scraper.external_ip)
    print('uptime: ' + str(scraper.uptime))
    print('bytes sent: ' + str(scraper.bytes_sent))
    print('bytes received: ' + str(scraper.bytes_received))
    print('bytes received / s: ' + str(scraper.transmission_rate))
    print('max bit rate: ' + str(scraper.max_bit_rate))
    print('max byte rate: ' + str(scraper.max_byte_rate))

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

if __name__ == '__main__':
  scraper = FritzScraper()
  scraper.print_status()

  mqtt = MqttConnection()
  try:
    mqtt.connect()
  except KeyboardInterrupt:
    print('Interrupt received, cleaning up...')
  finally:
    mqtt.disconnect()
