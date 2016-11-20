
import fritzscraper as fs
import mqttconnection as mqtt

if __name__ == '__main__':
  scraper = fs.FritzScraper()
  scraper.print_status()

  mqttConn = mqtt.MqttConnection()
  try:
    mqttConn.connect()
  except KeyboardInterrupt:
    print('Interrupt received, cleaning up...')
  finally:
    mqttConn.disconnect()
