# HomeMonitoring

This runs on my little (soon™ to be upgraded) "[Home Server](https://www.asus.com/Motherboards/AT3IONTI_DELUXE/)".

It currently features following containerized services:
- [InfluxDB](https://github.com/influxdata/influxdb) for data storage
- [cAdvisor](https://github.com/google/cadvisor) to collect docker container metrics
- [Telegraf](https://github.com/influxdata/telegraf) to collect host metrics
- [Telegraf MQTT Plugin](https://github.com/influxdata/telegraf/tree/master/plugins/inputs/mqtt_consumer) to subscribe to a [EmonHub](https://github.com/openenergymonitor/emonhub) MQTT topic
- [Grafana](https://github.com/grafana/grafana) to display the data in dashboards

... and much more to come.


# Current plans:

1. Add data from my [Freematics One](http://freematics.com/pages/products/freematics-one/) when it arrives
2. Add data scraped from my FritzBox
3. Add some thermometers / hygrometers around the house
