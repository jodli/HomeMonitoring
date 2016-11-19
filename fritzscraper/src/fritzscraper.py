#!/usr/bin/env python

import paho.mqtt.client as mqtt
import fritzconnection as fc

import time

FRITZ_IP_ADDRESS = '192.168.0.1'
FRITZ_TCP_PORT = 49000

class FritzScraper(object):

  def __init__(self, connection=None, address=FRITZ_IP_ADDRESS, port=FRITZ_TCP_PORT):
    super(FritzScraper, self).__init__()
    if connection is None:
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

if __name__ == '__main__':
  scraper = FritzScraper()
  scraper.print_status()
