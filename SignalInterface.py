import json

class RelayData():
    def __init__(self):
        self.value=False

    def receive_json(self, json_data):
        if "value" in json_data:
            self.value=json_data['value']
            self.data_updated=True

class TermostatData():
    def __init__(self):
        self.temperatur=0
        self.setpoint=0
        self.heating=False

    def receive_json(self, json_data):
        if "temperature" in json_data:
            self.temperatur=json_data['temperature']
            self.data_updated=True
        if "setPoint" in json_data:
            self.setpoint=json_data['setPoint']
            self.data_updated=True
        if "heating" in json_data:
            self.heating=json_data['heating']
        
    def get_temperatur_text(self):
        if (self.temperatur == None):
            return "--- °C"
        return f"{self.temperatur} °C"
            
class SignalInterface():
    def __init__(self, json_data):
        self.termostatData1=TermostatData()
        self.termostatData2=TermostatData()
        self.termostatData3=TermostatData()
        self.receive_json(json_data)
        
    def receive_json(self, json_data):
        self.data_updated=False
        if (json_data is not None):
            if "Termostat1" in json_data:
                self.termostatData1.receive_json(json_data['Termostat1'])
                self.data_updated=True
            if "Termostat2" in json_data:
                self.termostatData2.receive_json(json_data['Termostat2'])
                self.data_updated=True
            if "Termostat3" in json_data:
                self.termostatData3.receive_json(json_data['Termostat3'])
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
        if (self.termostatData1.temperatur == None):
            return "--- °C"
        return f"{self.termostartData1.temperatur} °C"
        
    def get_temperatur2_text(self):
        if (self.termostatData2.temperatur == None):
            return "--- °C"
        return f"{self.termostartData2.temperatur} °C"
        
    def get_temperatur3_text(self):
        if (self.termostatData3.temperatur == None):
            return "--- °C"
        return f"{self.termostartData3.temperatur} °C"
        
    def get_SP1_text(self):
        if (self.termostatData1.setpoint == None):
            return "--- °C"
        return f"(SP: {self.termostartData1.setpoint} °C)"
        
    def get_SP2_text(self):
        if (self.termostatData2.setpoint == None):
            return "--- °C"
        return f"(SP: {self.termostartData2.setpoint} °C)"
        
    def get_SP3_text(self):
        if (self.termostatData3.setpoint == None):
            return "--- °C"
        return f"(SP: {self.termostartData3.setpoint} °C)"

if __name__ == '__main__':
    SI=SignalInterface()
    SI.receive_json()
