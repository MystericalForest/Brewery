import serial
import json
from PyQt5.QtCore import QThread, pyqtSignal
import SignalData as SD

# Klasse til at læse fra serielporten i en separat tråd
class SerialThread(QThread):
    # Signal til at sende data tilbage til GUI'en
    new_data_signal = pyqtSignal(SD.SignalData)

    def __init__(self, port, baudrate=9600):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.running = True

    def run(self):
        # Åbn serielporten
        with serial.Serial(self.port, self.baudrate, timeout=1) as ser:
            while self.running:
                # Læs data fra serielporten
                data = ser.readline().decode('utf-8').strip()
                if data:
                    try:
                        # Antag at dataen er i JSON-format
                        json_data = json.loads(data)
                        signalData=SD.SignalData(json_data)
                        if (signalData.data_updated):
                             # Send temperaturdata til GUI'en
                            self.new_data_signal.emit(signalData)
                    except json.JSONDecodeError:
                        pass  # Hvis der er fejl i JSON, ignorer det

    def stop(self):
        self.running = False
        self.wait()

    def send_data(self, data):
        """
        Send data til serielporten.
        :param data: Dataen der skal sendes (kan være en hvilken som helst datatype, 
                     men vil blive konverteret til JSON).
        """
        try:
            # Konverter data til JSON (hvis muligt)
            json_data = json.dumps(data)
            # Åbn serielporten og send data
            with serial.Serial(self.port, self.baudrate, timeout=1) as ser:
                ser.write(json_data.encode('utf-8'))
                ser.write("\n".encode('utf-8'))
        except (serial.SerialException, json.JSONDecodeError) as e:
            print(f"Fejl ved sending af data: {e}")