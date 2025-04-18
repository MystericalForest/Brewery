import serial
import json
import time
import SignalData as SD
from PyQt5.QtCore import QObject, pyqtSignal

# Klasse til at læse fra serielporten i en separat tråd
class SerialConnector(QObject):
    # Signal til at sende data tilbage til GUI'en
    new_data_signal = pyqtSignal(SD.SignalData)
    
    def __init__(self, port, demo_mode=False, baudrate=115200):
        super().__init__()
        self.demo_mode=demo_mode
        if (self.demo_mode):
            print("Demo mode: No hardware connections")
        self.port = port
        self.baudrate = baudrate
        if not self.demo_mode:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(1)
            self.get_data()
        
    def __del__(self):
        if not self.demo_mode:
            self.ser.close()
        
    def set_led(self, value):
        data ={'action':"set_led",
               'value':value}
        self.send_data(data)
        return self.get_data()
        
    def get_temperature(self, termostat=4):
        data ={'action':"get_temperature",
               'value':termostat}
        self.send_data(data)
 #       json_data = json.loads(self.get_data())
 #       response = SD.SignalData(json_data)
 #       self.new_data_signal.emit(response)
        return #json_data
        
    def set_relay(self, relay, value):
        data ={'relay':relay,
               'state':value}
        self.send_data(data)
        return self.get_data()
        
    def set_enabled(self, termostat, value):
        data ={'thermostat':termostat,
               'enabled':value}
        self.send_data(data)
        return self.get_data()
        
    def set_sensor(self, termostat, sensor):
        data ={'thermostat':termostat,
               'sensor':sensor}
        self.send_data(data)
        return self.get_data()
        
        
    def set_power(self, termostat, value):
        data ={'thermostat':termostat,
               'power':value}
        self.send_data(data)
        return self.get_data()
        
    def set_setpoint1(self, temperatur):
        data ={'action':"setpoint_1",
               'value':temperatur}
        self.send_data(data)
        return self.get_data()
        
    def set_setpoint2(self, temperatur):
        data ={'action':"setpoint_2",
               'value':temperatur}
        self.send_data(data)
        return self.get_data()
        
    def set_setpoint3(self, temperatur):
        data ={'action':"setpoint_3",
               'value':temperatur}
        self.send_data(data)
        return self.get_data()
        
    def request_data(self):
        data ={'status': True}
        self.send_data(data)
        return self.get_data()
        
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

                self.ser.write(json_data.encode('utf-8'))
                self.ser.write("\n".encode('utf-8'))
            except (serial.SerialException, json.JSONDecodeError) as e:
                print(f"Fejl ved sending af data: {e}")
        
    def get_data(self):
        if not self.demo_mode:
            try:
                response=self.ser.readline()
                if response == None:
                    time.sleep(1)
                    response=self.ser.readline()
                return response.decode('utf-8').strip()
            except (serial.SerialException, json.JSONDecodeError) as e:
                print(f"Fejl ved sending af data: {e}")

# Hovedfunktion
def main():
    app = QApplication(sys.argv)

    window = TemperatureApp()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    ser=SerialConnector("/dev/ttyACM0", demo_mode=False, baudrate=115200)
#    for i in range(4):
#        print(ser.set_relay(i, True))
#        time.sleep(0.3)
#    for i in range(4):
#        print(ser.set_relay(3-i, False))
#        time.sleep(0.3)
#    time.sleep(1)
    print(ser.set_power(1, 20))
    print(ser.set_enabled(0, True))
    print(ser.set_enabled(0, False))
 #   print(ser.get_temperature())