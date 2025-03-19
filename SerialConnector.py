import serial
import json
import time
import SignalData as SD
from PyQt5.QtCore import QObject, pyqtSignal

# Klasse til at læse fra serielporten i en separat tråd
class SerialConnector(QObject):
    # Signal til at sende data tilbage til GUI'en
    new_data_signal = pyqtSignal(SD.SignalData)
    
    def __init__(self, port, baudrate=9600):
        super().__init__()
        if (port=='DEMO'):
            self.demo_mode=True
            print("Demo mode: No hardware connections")
        else:
            self.demo_mode=False
        self.port = port
        self.baudrate = baudrate
        if not self.demo_mode:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(1)
        
    def __del__(self):
        if not self.demo_mode:
            self.ser.close()
        
    def set_led(self, value):
        data ={'action':"set_led",
               'value':value}
        self.send_data(data)
        
    def get_temperature(self, termostat=4):
        data ={'action':"get_temperature",
               'value':termostat}
        self.send_data(data)
        json_data = json.loads(self.get_data())
        response = SD.SignalData(json_data)
        self.new_data_signal.emit(response)
        return json_data
        
    def set_relay_1(self, value):
        data ={'action':"set_led",
               'value':value}
        self.send_data(data)
        
    def set_setpoint1(self, temperatur):
        data ={'action':"setpoint_1",
               'value':temperatur}
        self.send_data(data)
        
    def set_setpoint2(self, temperatur):
        data ={'action':"setpoint_2",
               'value':temperatur}
        self.send_data(data)
        
    def set_setpoint3(self, temperatur):
        data ={'action':"setpoint_3",
               'value':temperatur}
        self.send_data(data)
        
    def send_data(self, data):
        """
        Send data til serielporten.
        :param data: Dataen der skal sendes (kan være en hvilken som helst datatype, 
                     men vil blive konverteret til JSON).
        """
        if not self.demo_mode:
            try:
                # Konverter data til JSON (hvis muligt)
                json_data = json.dumps(data)
                # Åbn serielporten og send data
                with serial.Serial(self.port, self.baudrate, timeout=1) as ser:
                    ser.write(json_data.encode('utf-8'))
                    ser.write("\n".encode('utf-8'))
            except (serial.SerialException, json.JSONDecodeError) as e:
                print(f"Fejl ved sending af data: {e}")
        
    def get_data(self):
        if not self.demo_mode:
            try:
                # Åbn serielporten og hent data
                with serial.Serial(self.port, self.baudrate, timeout=1) as ser:
                    response=ser.readline()
                    return response.decode('utf-8').strip()
            except (serial.SerialException, json.JSONDecodeError) as e:
                print(f"Fejl ved sending af data: {e}")
