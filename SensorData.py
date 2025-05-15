from datetime import datetime, timedelta

class SensorData():
    def __init__(self):
        self.last_datapoint = None
        self.dataserie = []
        
    def add_data(self, datapoint):
        self.last_datapoint = datapoint
        if ((datetime.now() - self.last_datapoint.time) > timedelta(minutes=1)): 
            self.dataserie.append(datapoint)
            if (len(self.dataserie > 200)):
                self.dataserie = self.dataserie[-200:]
            
    def get_graph_data(self):
        time = []
        temperature = []
        for idx, item in enumerate(self.dataserie):
            time.append(idx) #(item.time)
            temperature.append(item.temperature)
            
        return temperature, time