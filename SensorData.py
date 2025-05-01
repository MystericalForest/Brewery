class SensorDataPoint():
    def __init__(self):
        self.sensor_type=""
        self.temperature=-100
        self.errorflag=False
        self.errorDescription=""
        self.humidity=None
        
class SensorData():
    def __init__(self):
        self.last_datapoint = None
        self.dataserie = []
        
    def add_data(self, datapoint):
        self.last_datapoint = datapoint
        self.dataserie.append(datapoint)
        