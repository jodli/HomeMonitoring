# HomeMonitoring

This runs on my little (soon™ to be upgraded) "[Home Server](https://www.asus.com/Motherboards/AT3IONTI_DELUXE/)".

It currently features following containerized services:
- [InfluxDB](https://github.com/influxdata/influxdb) for data storage
- [Telegraf](https://github.com/influxdata/telegraf) to collect host metrics
- [Telegraf MQTT Consumer Plugin](https://github.com/influxdata/telegraf/tree/master/plugins/inputs/mqtt_consumer) subscribed to following topics:
  - My [EmonHub](https://github.com/openenergymonitor/emonhub) service to collect power usage data
  - My [FritzScraper](https://github.com/jodli/HomeMonitoring/tree/master/fritzscraper) service to collect data from my FritzBox 7490
- [Grafana](https://github.com/grafana/grafana) to display the data in dashboards

... and much more to come.
