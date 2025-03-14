import sys
import json
from PyQt5.QtCore import QTimer, Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QLineEdit, QSlider, QDialog
import SignalData as SD
import ChangeSetpointDialog
import SerialThreat as ST
import ButtonsWidget as BW, TermostatWidget as TW, HeaderWidget as HW, WatchWidget as WW, RelayWidget as RW
import random

# GUI Klasse
class TemperatureApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setpoint1=0
        self.setpoint2=0
        self.setpoint3=0

        self.initUI()

        # Opret en timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_temperature)  # Forbinder timerens signal til en slot
        self.timer.start(3000)  # Starter timeren og opdaterer hver 1000 ms (3 sekund)

    def initUI(self):
        super().__init__()

        # Initialiserer de forskellige widgets
        self.header = HW.HeaderWidget()
        self.termostat1 = TW.TermostatWidget("Spargevand")
        self.termostat2 = TW.TermostatWidget("Mæskegryde")
        self.termostat3 = TW.TermostatWidget("Kogegryde")
        self.buttons = BW.ButtonsWidget("Control")
        self.relays = RW.RelayWidget("Pumpe", "Lys", "Støvsuger", "Kran")
        self.watch = WW.WatchWidget("Mæsketid", "Kogetid", "Pause")
        self.watch.set_time(1000, 5000, 10000)

        # Opretter et overordnet layout og tilføjer widgets til det
        main_layout = QGridLayout()
        main_layout.addWidget(self.header, 0, 0, 1, 4)
        main_layout.addWidget(self.termostat1.get_widget(), 1, 0)
        main_layout.addWidget(self.termostat2.get_widget(), 1, 1)
        main_layout.addWidget(self.termostat3.get_widget(), 1, 2)
        main_layout.addWidget(self.buttons.get_widget(), 1, 3)
        main_layout.addWidget(self.relays, 2, 0, 1, 4)
        main_layout.addWidget(self.watch, 3, 0, 1, 4)

        self.setLayout(main_layout)
        # Sæt vinduets titel og størrelse
        self.setWindowTitle('Brew Control')
        self.setGeometry(100, 100, 800, 400)

    def update_temperature(self): #, data):
        # Opdater GUI'en med den modtagne temperatur
        self.termostat1.temperature_updated.emit(50+random.randrange(-5, 5),60)
        self.termostat2.temperature_updated.emit(75+random.randrange(-5, 5),78)
        self.termostat3.temperature_updated.emit(95+random.randrange(-2, 5),100) 
##        self.termostat1(data.get_temperatur1_text(),
##                        data.get_SP1_text(),
##                        data.heat1)
##        self.termostat2(data.get_temperatur1_text(),
##                        data.get_SP1_text(),
##                        data.heat1)
##        self.termostat3(data.get_temperatur1_text(),
##                        data.get_SP1_text(),
##                        data.heat1)
#        self.setpoint1=data.setpoint1
#        self.setpoint2=data.setpoint2
#        self.setpoint3=data.setpoint3
        
# Hovedfunktion
def main():
    app = QApplication(sys.argv)

    window = TemperatureApp()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
