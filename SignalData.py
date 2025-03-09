import json

class SignalData():
    def __init__(self, json_data):
        self.receive_json(json_data)
        
    def receive_json(self, json_data):
        self.data_updated=False
        if "Sensor1" in json_data:
            self.temperatur1=json_data['Sensor1']
            self.data_updated=True
        if "Sensor2" in json_data:
            self.temperatur2=json_data['Sensor2']
            self.data_updated=True
        if "Sensor3" in json_data:
            self.temperatur3=json_data['Sensor3']
            self.data_updated=True
        if "SP1" in json_data:
            self.setpoint1=json_data['SP1']
            self.data_updated=True
        if "SP2" in json_data:
            self.setpoint2=json_data['SP2']
            self.data_updated=True
        if "SP3" in json_data:
            self.setpoint3=json_data['SP3']
            self.data_updated=True
        if "Heat1" in json_data:
            self.heat1=json_data['Heat1']
            self.data_updated=True
        if "Heat2" in json_data:
            self.heat2=json_data['Heat2']
            self.data_updated=True
        if "Heat3" in json_data:
            self.heat3=json_data['Heat3']
            self.data_updated=True
        
    def get_temperatur1_text(self):
        if (self.temperatur1 == None):
            return "--- °C"
        return f"{self.temperatur1} °C"
        
    def get_temperatur2_text(self):
        if (self.temperatur2 == None):
            return "--- °C"
        return f"{self.temperatur2} °C"
        
    def get_temperatur3_text(self):
        if (self.temperatur3 == None):
            return "--- °C"
        return f"{self.temperatur3} °C"
        
    def get_SP1_text(self):
        if (self.setpoint1 == None):
            return "--- °C"
        return f"(SP: {self.setpoint1} °C)"
        
    def get_SP2_text(self):
        if (self.setpoint2 == None):
            return "--- °C"
        return f"(SP: {self.setpoint2} °C)"
        
    def get_SP3_text(self):
        if (self.setpoint3 == None):
            return "--- °C"
        return f"(SP: {self.setpoint3} °C)"
