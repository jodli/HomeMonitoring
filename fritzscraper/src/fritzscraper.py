#!/usr/bin/env python

import paho.mqtt.client as mqtt
import fritzconnection as fc

FRITZ_IP_ADDRESS = '192.168.0.1'
FRITZ_TCP_PORT = 49000

def scrape():
  print("Scraping...")

def connect_mqtt():
  print("Connecting to MQTT broker...")

class FritzScraper(object):

  def __init__(self, connection=None, address=FRITZ_IP_ADDRESS, port=FRITZ_TCP_PORT):
    super(FritzScraper, self).__init__()
    if connection is None:
      connection = fc.FritzConnection(address=address, port=port)
    self.connection = connection

  @property
  def modelname(self):
    return self.connection.modelname

  @property
  def is_linked(self):
    """Returns True if the FritzBox is physically linked to the provider."""
    status = self.connection.call_action('WANCommonInterfaceConfig', 'GetCommonLinkProperties')
    return status['NewPhysicalLinkStatus'] == 'Up'

  @property
  def is_connected(self):
    """Returns True if the FritzBox has established an internet-connection."""
    status = self.connection.call_action('WANIPConnection', 'GetStatusInfo')
    return status['NewConnectionStatus'] == 'Connected'

  @property
  def wan_access_type(self):
    """Returns connection-type: DSL, Cable."""
    return self.connection.call_action('WANCommonInterfaceConfig', 'GetCommonLinkProperties')['NewWANAccessType']

  @property
  def external_ip(self):
    """Returns the external ip-address."""
    return self.connection.call_action('WANIPConnection', 'GetExternalIPAddress')['NewExternalIPAddress']

  @property
  def uptime(self):
    """uptime in seconds."""
    return self.connection.call_action('WANIPConnection', 'GetStatusInfo')['NewUptime']

  def connect_fritz():
    print("Connecting to FritzBox...")

if __name__ == '__main__':
  connect_mqtt()
  scraper = FritzScraper()
  print('model: ' + scraper.modelname)
  print('linked: ' + str(scraper.is_linked))
  print('connected: ' + str(scraper.is_connected))
  print('wan access: ' + scraper.wan_access_type)
  print('external ip: ' + scraper.external_ip)
  print('uptime: ' + str(scraper.uptime))
  scrape()
