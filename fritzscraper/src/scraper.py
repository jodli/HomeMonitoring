#!/usr/bin/env python

import fritzconnection as fc
import fritzscrapercargo as fsc

import time

FRITZ_IP_ADDRESS = '192.168.0.1'
FRITZ_TCP_PORT = 49000

class Scraper(object):

  connection = None
  last_bytes_sent = 0
  last_bytes_received = 0
  last_traffic_call = 0.0
  fscargo = {}

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
  def max_bitrate(self):
    status = self.connection.call_action('WANCommonInterfaceConfig', 'GetCommonLinkProperties')
    downstream = status['NewLayer1DownstreamMaxBitRate']
    upstream = status['NewLayer1UpstreamMaxBitRate']
    return upstream, downstream

  def get_cargo(self):
    self.update_data()
    return self.fscargo

  def update_data(self):
    cargo = {}
    cargo["modelname"] = self.modelname
    cargo["is_linked"] = self.is_linked
    cargo["is_connected"] = self.is_connected
    cargo["wan_access_type"] = self.wan_access_type
    cargo["external_ip"] = self.external_ip
    cargo["uptime"] = self.uptime
    cargo["bytes received"] = self.bytes_received
    cargo["bytes sent"] = self.bytes_sent
    transmission_rate_upstream, transmission_rate_downstream = self.transmission_rate
    cargo["transmission_rate_upstream"] = transmission_rate_upstream
    cargo["transmission_rate_downstream"] = transmission_rate_downstream
    max_bitrate_upstream, max_bitrate_downstream = self.max_bitrate
    cargo["max_bitrate_upstream"] = max_bitrate_upstream
    cargo["max_bitrate_downstream"] = max_bitrate_downstream

    self.fscargo = fsc.FritzScraperCargo(cargo)

  def print_status(self):
    print("time: " + str(self.fscargo.timestamp))
    for name, value in self.fscargo.cargo.items():
      print(name + ": " + str(value))
