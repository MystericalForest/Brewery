import json

class SignalDataRelays():
    def __init__(self):
        self.relay_1=False
        self.relay_2=False
        self.relay_3=False
        self.relay_4=False

    def receive_json(self, json_data):
        self.relay_1=json_data[0]
        self.relay_2=json_data[1]
        self.relay_3=json_data[2]
        self.relay_4=json_data[3]

class SignalDataSensor():
    def __init__(self):
        self.sensor_type=""
        self.temperature=-100
        self.erroflag=False
        self.errorDescription=""
        self.humidity=None

    def receive_json(self, json_data):
        if "Type" in json_data:
            self.sensorType=json_data['Type']
        if "Temperature" in json_data:
            self.temperatur=json_data['Temperature']
        if "ErrorFlag" in json_data:
            self.erroflag=json_data['ErrorFlag']
        if "ErrorDescription" in json_data:
            self.errorDescription=json_data['ErrorDescription']
        if "Humidity" in json_data:
            self.humidity=json_data['Humidity']

class SignalDataTermostat():
    def __init__(self):
        self.temperatur=0
        self.setpoint=0
        self.enabled=True
        self.power=50
        self.manual=True
        self.heating=False

    def receive_json(self, json_data):
        if "Manual" in json_data:
            self.manual=json_data['Manual']
            self.data_updated=True
        if "Temperature" in json_data:
            self.temperatur=json_data['Temperature']
            self.data_updated=True
        if "Setpoint" in json_data:
            self.setpoint=json_data['Setpoint']
            self.data_updated=True
        if "Heating" in json_data:
            self.heating=json_data['Heating']
            self.data_updated=True
        if "Power" in json_data:
            self.power=json_data['Power']
            self.data_updated=True
        if "Enabled" in json_data:
            self.enabled=json_data['Enabled']
            self.data_updated=True
        
    def get_temperatur_text(self):
        if (self.temperatur == None):
            return "--- °C"
        return f"{self.temperatur} °C"
            
class SignalData():
    def __init__(self, json_data):
        self.sensorData1=SignalDataSensor()
        self.sensorData2=SignalDataSensor()
        self.sensorData3=SignalDataSensor()
        self.sensorData4=SignalDataSensor()
        self.sensorData5=SignalDataSensor()
        self.sensorData6=SignalDataSensor()
        self.sensorData7=SignalDataSensor()
        self.termostatData1=SignalDataTermostat()
        self.termostatData2=SignalDataTermostat()
        self.termostatData3=SignalDataTermostat()
        self.relays=SignalDataRelays()
        self.receive_json(json_data)
        
    def receive_json(self, json_data):
        self.data_updated=False
        if (json_data is not None):
            data = json.loads(json_data)
            if "relays" in data:
                self.relays.receive_json(data['relays'])
                self.data_updated=True
            if "Termostater" in data:
                termo_data=data['Termostater']
                if "Termostat1" in termo_data:
                    self.termostatData1.receive_json(termo_data['Termostat1'])
                    self.data_updated=True
                if "Termostat2" in termo_data:
                    self.termostatData2.receive_json(termo_data['Termostat2'])
                    self.data_updated=True
                if "Termostat3" in termo_data:
                    self.termostatData3.receive_json(termo_data['Termostat3'])
                    self.data_updated=True
            if "Sensor" in data:
                sensor_data=data['Sensor']
                if "Sensor1" in sensor_data:
                    self.sensorData1.receive_json(sensor_data['Sensor1'])
                    self.data_updated=True
                if "Sensor2" in sensor_data:
                    self.sensorData2.receive_json(sensor_data['Sensor2'])
                    self.data_updated=True
                if "Sensor3" in sensor_data:
                    self.sensorData3.receive_json(sensor_data['Sensor3'])
                    self.data_updated=True
                if "Sensor4" in sensor_data:
                    self.sensorData4.receive_json(sensor_data['Sensor4'])
                    self.data_updated=True
                if "Sensor5" in sensor_data:
                    self.sensorData5.receive_json(sensor_data['Sensor5'])
                    self.data_updated=True
                if "Sensor6" in sensor_data:
                    self.sensorData6.receive_json(sensor_data['Sensor6'])
                    self.data_updated=True
                if "RoomSensor" in sensor_data:
                    self.sensorData7.receive_json(sensor_data['RoomSensor'])
                    self.data_updated=True
##            if "Sensor2" in data:
##                self.temperatur2=data['Sensor2']
##                self.data_updated=True
##            if "Sensor3" in data:
##                self.temperatur3=data['Sensor3']
##                self.data_updated=True
##            if "SP1" in data:
##                self.setpoint1=data['SP1']
##                self.data_updated=True
##            if "SP2" in data:
##                self.setpoint2=data['SP2']
##                self.data_updated=True
##            if "SP3" in data:
##                self.setpoint3=data['SP3']
##                self.data_updated=True
##            if "Heat1" in data:
##                self.heat1=data['Heat1']
##                self.data_updated=True
##            if "Heat2" in data:
##                self.heat2=data['Heat2']
##                self.data_updated=True
##            if "Heat3" in data:
##                self.heat3=data['Heat3']
##                self.data_updated=True
        
    def get_temperatur1_text(self):
        if (self.termostatData1.enabled == False):
            return "-x- °C"
        if (self.termostatData1.temperatur == None):
            return "--- °C"
        return f"{self.termostartData1.temperatur} °C"
        
    def get_temperatur2_text(self):
        if (self.termostatData2.enabled == False):
            return "-x- °C"
        if (self.termostatData2.temperatur == None):
            return "--- °C"
        return f"{self.termostartData2.temperatur} °C"
        
    def get_temperatur3_text(self):
        if (self.termostatData3.enabled == False):
            return "-x- °C"
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
