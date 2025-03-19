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
    def __init__(self, serialConnector):
        super().__init__()
        self.settings = QSettings("VestervangBryglaug", "BrewControl")
        self.serialConnector = serialConnector
        self.load_settings()
        self.setpoint1=0
        self.setpoint2=0
        self.setpoint3=0
        self.termoData = TW.TermoDataClass()

        self.initUI()

        # Opret en timer
        if (not self.serialConnector.demo_mode):
            timer = QTimer(self, interval=3000, timeout=self.update_temperature)
            timer.start()

        self.serialConnector.new_data_signal.connect(self.update_temperature)
        
    def initUI(self):
        super().__init__()

        # Initialiserer de forskellige widgets
        self.header = HW.HeaderWidget()
        self.termostat1 = TW.TermostatWidget(self.termo_1_name)
        self.termostat2 = TW.TermostatWidget(self.termo_2_name)
        self.termostat3 = TW.TermostatWidget(self.termo_3_name)
        self.buttons = BW.ButtonsWidget("Control")
        self.relays = RW.RelayWidget(self,"Pumpe", "Lys", "Støvsuger", "Kran")
        self.watch = WW.WatchWidget("Mæsketid", "Kogetid", "Pause")
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
        self.port = self.settings.value("port", "")
        self.termo_1_name = self.settings.value("termo_1_name", "")
        self.termo_2_name = self.settings.value("termo_2_name", "")
        self.termo_3_name = self.settings.value("termo_3_name", "")
        self.watch_1_name = self.settings.value("watch_1_name", "")
        self.watch_2_name = self.settings.value("watch_2_name", "")
        self.watch_3_name = self.settings.value("watch_3_name", "")
        self.demo_mode = self.settings.value("demo_mode", False, type=bool)
    
    def set_relay_1(self, value):
        data=SignalData.SignalData(self.serialConnector.set_relay_1(value))
        print(data)

    def update_temperature(self): #, data):
        data=SignalData.SignalData(self.serialConnector.get_temperature())
        # Opdater GUI'en med den modtagne temperatur
        self.termostat1.temperature_updated.emit(data.termostatData1.temperatur,data.termostatData1.setpoint)
        self.termostat2.temperature_updated.emit(data.termostatData2.temperatur,data.termostatData2.setpoint)
        self.termostat3.temperature_updated.emit(data.termostatData3.temperatur,data.termostatData3.setpoint) 

# Hovedfunktion
def main():
    app = QApplication(sys.argv)
    #serialConnector = SD.SerialConnector('/dev/ttyACM0')
    serialConnector = SD.SerialConnector('DEMO')

    window = TemperatureApp(serialConnector)
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
