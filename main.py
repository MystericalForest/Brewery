import sys
import json
from PyQt5.QtCore import QTimer, Qt, QThread, pyqtSignal, QSettings
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QLineEdit, QSlider, QDialog
import SignalData as SD
import ChangeSetpointDialog
import SerialThreat as ST
import ButtonsWidget as BW, TermostatWidget as TW, HeaderWidget as HW, WatchWidget as WW, RelayWidget as RW
import random
import SerialConnector as SD, SignalData

# GUI Klasse
class TemperatureApp(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("VestervangBryglaug", "BrewControl")
        self.load_settings()
#        self.serialConnector = SD.SerialConnector("/dev/ttyACM0", demo_mode=False, baudrate=115200)
        self.serialConnector = SD.SerialConnector(self.port, demo_mode=self.demo_mode, baudrate=115200)
#        self.serialConnector = serialConnector
        self.setpoint1=0
        self.setpoint2=0
        self.setpoint3=0
        self.termoData = TW.TermoDataClass()

        self.initUI()
        self.set_sensor(0, self.termo_1_sensor)
        self.set_sensor(1, self.termo_2_sensor)
        self.set_sensor(2, self.termo_3_sensor)

        # Opret en timer
        if (not self.demo_mode):
            timer = QTimer(self, interval=3000, timeout=self.update_temperature)
            timer.start()

#        self.serialConnector.new_data_signal.connect(self.update_temperature)
        
    def initUI(self):
        super().__init__()

        # Initialiserer de forskellige widgets
        self.header = HW.HeaderWidget()
        self.termostat1 = TW.TermostatWidget(self, 0, self.termo_1_name, self.termo_1_sensor)
        self.termostat2 = TW.TermostatWidget(self, 1, self.termo_2_name, self.termo_2_sensor)
        self.termostat3 = TW.TermostatWidget(self, 2, self.termo_3_name, self.termo_3_sensor)
        self.buttons = BW.ButtonsWidget(self, "Control")
        self.relays = RW.RelayWidget(self, "Pumpe", "Lys", "Støvsuger", "Kran")
        self.watch = WW.WatchWidget(self.watch_1_name, self.watch_2_name, self.watch_3_name)
        self.watch.set_time(1000, 5000, 10000)

        # Opretter et overordnet layout og tilføjer widgets til det
        main_layout = QGridLayout()
        main_layout.addWidget(self.header, 0, 0, 1, 4)
        main_layout.addWidget(self.termostat1.get_widget(), 1, 0)
        main_layout.addWidget(self.termostat2.get_widget(), 1, 1)
        main_layout.addWidget(self.termostat3.get_widget(), 1, 2)
        main_layout.addWidget(self.relays, 1, 3)
        main_layout.addWidget(self.watch, 2, 0, 1, 3)
        main_layout.addWidget(self.buttons.get_widget(), 2, 3)

        self.setLayout(main_layout)
        # Sæt vinduets titel og størrelse
        self.setWindowTitle('Brew Control')
        self.setGeometry(100, 100, 800, 400)

    def load_settings(self):
        self.port = "/dev/ttyACM0" #self.settings.value("port", "/dev/ttyACM0")
        self.termo_1_name = self.settings.value("termo_1_name", "Spargevand")
        self.termo_1_sensor = int(self.settings.value("termo_1_sensor", 0))
        self.termo_2_name = self.settings.value("termo_2_name", "Mæskegryde")
        self.termo_2_sensor = int(self.settings.value("termo_2_sensor", 0))
        self.termo_3_name = self.settings.value("termo_3_name", "Kogegryde")
        self.termo_3_sensor = int(self.settings.value("termo_3_sensor", 0))
        self.watch_1_name = self.settings.value("watch_1_name", "Mæsketid")
        self.watch_2_name = self.settings.value("watch_2_name", "Kogetid")
        self.watch_3_name = self.settings.value("watch_3_name", "Pause")
        self.demo_mode = self.settings.value("demo_mode", False, type=bool)
    
    def set_relay(self, relay, value):
        data=SignalData.SignalData(self.serialConnector.set_relay(relay, value))
        self.update_data(data)
    
    def set_enabled(self, termostat_id, value):
        data=SignalData.SignalData(self.serialConnector.set_enabled(termostat_id, value))
        self.update_data(data)
    
    def set_sensor(self, termostat_id, sensor):
        data=SignalData.SignalData(self.serialConnector.set_sensor(termostat_id, sensor))
        self.update_data(data)
    
    def set_power(self, termostat_id, value):
        data=SignalData.SignalData(self.serialConnector.set_power(termostat_id, value))
        self.update_data(data)
        
    def update_data(self, data):
        self.relays.update_state(data)
        self.termostat1.update_data(data.termostatData1)
        self.termostat2.update_data(data.termostatData2)
        self.termostat3.update_data(data.termostatData3)

    def update_temperature(self): #, data):
        data=SignalData.SignalData(self.serialConnector.request_data())
        self.update_data(data)
#        data=SignalData.SignalData(self.serialConnector.get_temperature())
        # Opdater GUI'en med den modtagne temperatur
#        self.termostat1.temperature_updated.emit(data.termostatData1.temperatur,data.termostatData1.setpoint)
#        self.termostat2.temperature_updated.emit(data.termostatData2.temperatur,data.termostatData2.setpoint)
#        self.termostat3.temperature_updated.emit(data.termostatData3.temperatur,data.termostatData3.setpoint)
    
#    def parse_json(self, json_data):
#        data=json.loads(json_data)
#        print(data["Termostat1"])

# Hovedfunktion
def main():
    app = QApplication(sys.argv)

    window = TemperatureApp()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
