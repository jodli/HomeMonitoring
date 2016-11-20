
class FritzScraperCargo(object):
  timestamp = 0.0
  names = []
  values = []

  def __init__(self, timestamp, names, values):
    self.timestamp = float(timestamp)
    self.names = names
    self.values = values
