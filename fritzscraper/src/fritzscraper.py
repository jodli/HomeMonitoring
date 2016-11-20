
import scraper as fs
import mqttconnection as mqtt
import signal
import sys
import time

INTERVAL = 5.0

class FritzScraper(object):

  def __init__(self):
    self._exit = False
    signal.signal(signal.SIGTERM, self._sigterm_handler)

    self._scraper = fs.Scraper()
    self._mqttConnection = mqtt.MqttConnection()

  def _sigterm_handler(self, signal, frame):
    print("SIGTERM received")
    self._exit = True

  def run(self):
    while not self._exit:
      self._mqttConnection.connect()
      fscargo = self._scraper.get_cargo()
      self._mqttConnection.publish(fscargo)

      print("Sleep for " + str(INTERVAL) + "s")
      sys.stdout.flush()
      time.sleep(INTERVAL)

  def close(self):
    print("Cleaning up...")
    self._mqttConnection.disconnect()

if __name__ == '__main__':

  try:
    print("Creating FritzScraper...")
    fritzScraper = FritzScraper()
  except Exception as e:
    sys.exit("Could not create FritzScraper: " + str(e))
  else:
    fritzScraper.run()

    fritzScraper.close()
