from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QLineEdit, QSlider, QDialog, QGroupBox
import ChangeSetpointDialog, SettingsDialog

class ButtonsWidget(QWidget):
    def __init__(self, title):
        super().__init__()

        self.ret_SP_button = QPushButton('Ret Setpoint', self)
        self.ret_SP_button.clicked.connect(self.open_setpoint_dialog) 
        self.ret_SP_button.resize(150, 100) 
 
        self.settings_button = QPushButton('Settings', self)
        self.settings_button.clicked.connect(self.open_setting_dialog)
        self.settings_button.resize(150, 100) 

        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.start_reading)
        self.start_button.resize(150, 100) 
 
        self.stop_button = QPushButton('Stop', self)
        self.stop_button.clicked.connect(self.stop_reading)
        self.stop_button.resize(150, 100) 

        # Opretter en gruppe til formområdet
        self.group_box = QGroupBox(title)

        # Opret layout
        layout = QGridLayout()
        layout.addWidget(self.ret_SP_button,0,0)
        layout.addWidget(self.settings_button,1,0)
        layout.addWidget(self.start_button,2,0)
        layout.addWidget(self.stop_button,3,0)
        self.group_box.setLayout(layout)

    def open_setpoint_dialog(self):
        # Åbner det nye vindue
        self.changeSetpointDialog = ChangeSetpointDialog.ChangeSetpointDialog(self.setpoint1, self.setpoint2, self.setpoint3)
        self.changeSetpointDialog.show()
  #      self.changeSetpointDialog.values_transferred.connect(self.ret_setpoint)

    def open_setting_dialog(self):
        # Åbner det nye vindue
        self.SettingsDialog = SettingsDialog.SettingsDialog()
        self.SettingsDialog.show()
 #       self.SettingsDialog.values_transferred.connect(self.ret_setpoint)

    def ret_setpoint(self, setpoint1, setpoint2, setpoint3):
        Data ={'Setpoint1':setpoint1,
               'Setpoint2':setpoint2,
               'Setpoint3':setpoint3}
        
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

    def get_widget(self):
        return self.group_box
