
import scraper as fs
import mqttconnection as mqtt
import signal
import sys
import time

class FritzScraper(object):

  def __init__(self):
    self._exit = False
    signal.signal(signal.SIGTERM, self._sigterm_handler)

    self._scraper = fs.Scraper()
    #self._mqttConnection = mqtt.MqttConnection()

    #self._mqttConnection.connect()

  def _sigterm_handler(self, signal, frame):
    print("SIGTERM received")
    self._exit = True

  def run(self):
    while not self._exit:
      print("Working...")
      sys.stdout.flush()
      time.sleep(1)
      #self._scraper.print_status()

  def close(self):
    print("Cleaning up...")

if __name__ == '__main__':

  try:
    print("Creating FritzScraper...")
    fritzScraper = FritzScraper()
  except Exception as e:
    sys.exit("Could not start FritzScraper: " + str(e))
  else:
    print("Start scraping...")
    fritzScraper.run()

    fritzScraper.close()
