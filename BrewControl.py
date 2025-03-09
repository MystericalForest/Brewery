import sys
import json
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QLineEdit, QSlider, QDialog
import SignalData as SD
import ChangeSetpointDialog
import SerialThreat as ST
        
# GUI Klasse
class TemperatureApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setpoint1=0
        self.setpoint2=0
        self.setpoint3=0

        self.initUI()

    def initUI(self):
        # Opret GUI-elementer
        self.header1 = QLabel("Spargevand", self)
        self.header1.setAlignment(Qt.AlignCenter)
        self.header1.setStyleSheet("font-size: 30px;")
        
        self.temp_label1 = QLabel("-- °C", self)
        self.temp_label1.setAlignment(Qt.AlignCenter)
        self.temp_label1.setStyleSheet("font-size: 72px;")
        
        self.sp_label1 = QLabel("(SP: -- °C)", self)
        self.sp_label1.setAlignment(Qt.AlignCenter)
        self.sp_label1.setStyleSheet("font-size: 30px;")
        
        self.statustext1 = QLabel("Varmer", self)
        self.statustext1.setAlignment(Qt.AlignCenter)
        self.statustext1.setStyleSheet("font-size: 20px;background-color: yellow")
        self.statustext1.setEnabled(True)
        
        self.header2 = QLabel("Mæskegryde", self)
        self.header2.setAlignment(Qt.AlignCenter)
        self.header2.setStyleSheet("font-size: 30px;")
        
        self.temp_label2 = QLabel("-- °C", self)
        self.temp_label2.setAlignment(Qt.AlignCenter)
        self.temp_label2.setStyleSheet("font-size: 72px;")
        
        self.sp_label2 = QLabel("(SP: -- °C)", self)
        self.sp_label2.setAlignment(Qt.AlignCenter)
        self.sp_label2.setStyleSheet("font-size: 30px;")
        
        self.statustext2 = QLabel("Varmer", self)
        self.statustext2.setAlignment(Qt.AlignCenter)
        self.statustext2.setStyleSheet("font-size: 20px;background-color: yellow")
        self.statustext2.setEnabled(False)
        
        self.header3 = QLabel("Kogegryde", self)
        self.header3.setAlignment(Qt.AlignCenter)
        self.header3.setStyleSheet("font-size: 30px;")
        
        self.temp_label3 = QLabel("-- °C", self)
        self.temp_label3.setAlignment(Qt.AlignCenter)
        self.temp_label3.setStyleSheet("font-size: 72px;")
        
        self.sp_label3 = QLabel("(SP: -- °C)", self)
        self.sp_label3.setAlignment(Qt.AlignCenter)
        self.sp_label3.setStyleSheet("font-size: 30px;")
        
        self.statustext3 = QLabel("Varmer", self)
        self.statustext3.setAlignment(Qt.AlignCenter)
        self.statustext3.setStyleSheet("font-size: 20px;background-color: yellow")
        self.statustext3.setEnabled(False)

        self.ret_SP_button = QPushButton('Ret Setpoint', self)
        self.ret_SP_button.clicked.connect(self.open_setpoint_dialog)

        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.start_reading)
 
        self.stop_button = QPushButton('Stop', self)
        self.stop_button.clicked.connect(self.stop_reading)

        # Opret layout
        layout = QGridLayout()
        layout.addWidget(self.header1,0,0)
        layout.addWidget(self.temp_label1,1,0)
        layout.addWidget(self.sp_label1,2,0)
        layout.addWidget(self.statustext1,3,0)
        layout.addWidget(self.header2,0,1)
        layout.addWidget(self.temp_label2,1,1)
        layout.addWidget(self.sp_label2,2,1)
        layout.addWidget(self.statustext2,3,1)
        layout.addWidget(self.header3,0,2)
        layout.addWidget(self.temp_label3,1,2)
        layout.addWidget(self.sp_label3,2,2)
        layout.addWidget(self.statustext3,3,2)
        layout.addWidget(self.ret_SP_button,4,0)
        layout.addWidget(self.start_button,4,1)
        layout.addWidget(self.stop_button,4,2)
        self.setLayout(layout)

        # Sæt vinduets titel og størrelse
        self.setWindowTitle('Brew Control')
        self.setGeometry(100, 100, 800, 300)
        self.serial_thread = None

    def open_setpoint_dialog(self):
        # Åbner det nye vindue
        self.changeSetpointDialog = ChangeSetpointDialog.ChangeSetpointDialog(self.setpoint1, self.setpoint2, self.setpoint3)
        print(self.setpoint1)
        self.changeSetpointDialog.values_transferred.connect(self.ret_setpoint)
        self.changeSetpointDialog.exec_()

    def ret_setpoint(self, setpoint1, setpoint2, setpoint3):
        Data ={'Setpoint1':setpoint1,
               'Setpoint2':setpoint2,
               'Setpoint3':setpoint3}
        print(Data)
        self.serial_thread.send_data(Data)
        self.setpoint1=setpoint1
        self.setpoint2=setpoint2
        self.setpoint3=setpoint3

    def start_reading(self):
        # Start læsning fra serielporten i en separat tråd
        self.serial_thread = ST.SerialThread('/dev/ttyACM0')  # Erstat med den korrekte port
        self.serial_thread.new_data_signal.connect(self.update_temperature)
        self.serial_thread.start()

    def stop_reading(self):
        # Stop læsning fra serielporten
        if self.serial_thread:
            self.serial_thread.stop()
            self.serial_thread = None

    def update_temperature(self, data):
        # Opdater GUI'en med den modtagne temperatur
        self.temp_label1.setText(data.get_temperatur1_text())
        self.temp_label2.setText(data.get_temperatur2_text())
        self.temp_label3.setText(data.get_temperatur3_text())
        self.sp_label1.setText(data.get_SP1_text())
        self.sp_label2.setText(data.get_SP2_text())
        self.sp_label3.setText(data.get_SP3_text())
        self.setpoint1=data.setpoint1
        self.setpoint2=data.setpoint2
        self.setpoint3=data.setpoint3
        self.statustext1.setEnabled(data.heat1)
        self.statustext2.setEnabled(data.heat2)
        self.statustext3.setEnabled(data.heat3)

#    def receive_setpoint_values(self, setpoint1, setpoint2, setpoint3):
#        pass
#         # Modtager værdierne fra sliders og opdaterer labels
#         self.value_label1.setText(f"Slider 1: {value1}")
#         self.value_label2.setText(f"Slider 2: {value2}")
#         self.value_label3.setText(f"Slider 3: {value3}")
        
# Hovedfunktion
def main():
    app = QApplication(sys.argv)

    window = TemperatureApp()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
