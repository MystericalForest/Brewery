from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QDial, QLineEdit, QSlider, QDialog, QGroupBox
import ChangeSetpointDialog, ChangePowerDialog, SettingsDialog
from datetime import datetime, timedelta
import TermostatGraf2 as TermostatGraf
import csv

class DataLogger:
    def __init__(self):
        self.log = []  # Gemmer data i hukommelsen som en liste af dicts

    def log_data(self, data):
        last_entry=self.get_last_entry()

        if last_entry is None:
            self.log.append({
                'timestamp': datetime.now(),
                'temperatur': data.temperatur,
                'setpoint': data.setpoint,
                'manual': data.manual,
                'heating': data.heating,
                'power': data.power
            })
        else:
            if (datetime.now() - last_entry["timestamp"] > timedelta(minutes=1)):
                changed_data=True if ((last_entry["setpoint"] != data.setpoint) or (last_entry["heating"] != data.heating)  or (last_entry["manual"] != data.manual)) else False
                if (changed_data):
                    self.log.append({
                        'timestamp': last_entry["timestamp"],
                        'temperatur': last_entry["temperatur"],
                        'setpoint': data.setpoint,
                        'manual': data.manual,
                        'heating': data.heating,
                        'power': last_entry["power"]
                    })

                self.log.append({
                    'timestamp': datetime.now(),
                    'temperatur': data.temperatur,
                    'setpoint': data.setpoint,
                    'manual': data.manual,
                    'heating': data.heating,
                    'power': data.power
                })

    def get_log(self):
        return self.log

    def get_last_entry(self):
        if len(self.log)==0:
            return
        return self.log[-1]
    
    def save_to_file(self, filename='data_log.csv'):
        with open(filename, mode='w', newline='') as file:
            fieldnames = ['timestamp', 'temperatur', 'setpoint', 'manual', 'heating', 'power']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            writer.writeheader()
            
            for entry in self.log:
                entry_copy = entry.copy()
                entry_copy['timestamp'] = entry_copy['timestamp'].isoformat()
                writer.writerow(entry_copy)
    
class TermoData():
    def __init__(self):
        self.temperature=0
        self.setpoint=0
        self.heating=False

class ClickableLabel(QLabel):
    clicked = pyqtSignal()
    
    def mousePressEvent(self, event):
        self.clicked.emit()
        
class TermoDataClass(QObject):
    # Signal, der bliver sendt, når dataene ændres
    dataChanged = pyqtSignal(TermoData)

    def __init__(self):
        super().__init__()
        self.data=TermoData()

    def update_data(self, temperature, setpoint, heating):
        self.data.temperature=temperature
        self.data.setpoint=setpoint
        self.data.heating=heating
        # Emit signalet med den nye værdi
        self.dataChanged.emit(self.data)
         
class TermostatWidget(QWidget):

    def __init__(self, parent, termostat_id, title, sensor_id):
        super().__init__()
        self.title = title
        self._id = termostat_id
        self.sensor_id = sensor_id
        self.parent = parent
        self.temperature=0
        self.heating=False
        self.setpoint=0

        self.data_logger = DataLogger()
        self.on_button = QPushButton("Off", self)
        self.on_button.setCheckable(True) # setting checkable to true
        self.on_button.clicked.connect(self.changeState) # setting calling method by button
        self.on_button.setStyleSheet("background-color : lightgrey") # setting default color of button to light-blue
        self.on_button.setChecked(False)
        
        self.header1 = QLabel(title, self)
        self.header1.setAlignment(Qt.AlignCenter)
        self.header1.setStyleSheet("font-size: 30px;")

        self.create_auto_power()
        self.create_manual_power()
        
        self.sensor_label = QLabel(f"Sensor: {self.sensor_id}", self)
        self.sensor_label.setAlignment(Qt.AlignCenter)
        self.sensor_label.setStyleSheet("font-size: 24px;")
 
        # Opretter en gruppe til formområdet
        self.group_box = QGroupBox(title)

        # Opret layout
        self.layout = QGridLayout()
        self.layout.addWidget(self.on_button,0,0)
        self.layout.addWidget(self.header1,1,0)
        if (self.sensor_id == 0):
            self.layout.addWidget(self.power_dial, 2, 0)
            self.layout.addWidget(self.power_label, 3, 0)
        else:
            self.layout.addWidget(self.temp_label,2,0)
            self.layout.addWidget(self.sp_label,3,0)
            self.layout.addWidget(self.statustext,4,0)
 #           self.layout.addWidget(self.setpoint_button,5,0)
        self.layout.addWidget(self.sensor_label,6,0)
        self.group_box.setLayout(self.layout)

    def set_title(self, title):
        self.title = title
        self.header1.setText(self.title)

    def set_sensor_id(self, sensor_id):
        if ((self.sensor_id == 0) and (sensor_id != 0)):
            self.layout.removeWidget(self.power_dial)
            self.layout.removeWidget(self.power_label)
            self.power_dial.deleteLater()
            self.power_label.deleteLater()
            self.create_auto_power()
            self.layout.addWidget(self.temp_label,2,0)
            self.layout.addWidget(self.sp_label,3,0)
            self.layout.addWidget(self.statustext,4,0)
#            self.layout.addWidget(self.setpoint_button,5,0)
        if ((self.sensor_id != 0) and (sensor_id == 0)):
            self.layout.removeWidget(self.temp_label)
            self.layout.removeWidget(self.sp_label)
            self.layout.removeWidget(self.statustext)
#            self.layout.removeWidget(self.setpoint_button)
#            self.setpoint_button.deleteLater()
            self.sp_label.deleteLater()
            self.statustext.deleteLater()
            self.temp_label.deleteLater()
            self.create_manual_power()
            self.layout.addWidget(self.power_dial, 2, 0)
            self.layout.addWidget(self.power_label, 3, 0)
        self.sensor_id = sensor_id
        self.sensor_label.setText(f"Sensor: {self.sensor_id}")
        self.parent.set_sensor(self._id, self.sensor_id)

    def updateLabel(self):
        # Opdaterer labelen med den aktuelle værdi fra drejeknappen
        self.power_label.setText(f"{self.power_dial.value()} %")
        if self.on_button.isChecked():
            self.parent.set_power(self._id, self.power_dial.value())

    def create_auto_power(self):   
        self.temp_label = ClickableLabel("-- °C", self)
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.temp_label.setStyleSheet("font-size: 72px;")
        self.temp_label.clicked.connect(self.open_termostat_graf)
        
        self.sp_label = ClickableLabel("(SP: -- °C)", self)
        self.sp_label.setAlignment(Qt.AlignCenter)
        self.sp_label.setStyleSheet("font-size: 30px;")
        self.sp_label.clicked.connect(self.open_setpoint_dialog) # setting calling method
        
        self.statustext = QLabel("Varmer", self)
        self.statustext.setAlignment(Qt.AlignCenter)
        self.statustext.setStyleSheet("font-size: 20px;background-color: yellow")
        self.statustext.setEnabled(True)
        
 #       self.setpoint_button = QPushButton("Ret Setpoint", self)
 #       self.setpoint_button.clicked.connect(self.open_setpoint_dialog) # setting calling method by button
        
    def create_manual_power(self):        
        self.power_dial = QDial(self)
        self.power_dial.setRange(0, 100)
        self.power_dial.setValue(50)

        self.power_label = ClickableLabel("50 %", self)
        self.power_label.setAlignment(Qt.AlignCenter)
        self.power_label.setStyleSheet("font-size: 30px;")
        self.power_label.clicked.connect(self.open_power_dialog) # setting calling method by button

        # Forbinder signalet til ændring af værdien med en slot (metode)
        self.power_dial.valueChanged.connect(self.updateLabel)
        
    def open_termostat_graf(self):
        # Åbner det nye vindue
        self.TermostatGraf = TermostatGraf.TermostatGraf(self.title, self.data_logger, parent=self)
        self.TermostatGraf.show()
        
    def open_setpoint_dialog(self):
        # Åbner det nye vindue
        self.ChangeSetpointDialog = ChangeSetpointDialog.ChangeSetpointDialog(self.title, 50)
        if self.ChangeSetpointDialog.exec_()  == QDialog.Accepted:
            self.update_setpoint(self.ChangeSetpointDialog.slider.value())
            self.setpoint=self.ChangeSetpointDialog.slider.value()

    def update_setpoint(self, setpoint):
        self.setpoint=setpoint
        self.update_temperature(50, setpoint)
        self.parent.set_setpoint(self._id, setpoint)
            
    def open_power_dialog(self):
        # Åbner det nye vindue
        self.ChangePowerDialog = ChangePowerDialog.ChangePowerDialog(self.title, 50)
        if self.ChangePowerDialog.exec_()  == QDialog.Accepted:
            self.power_dial.setValue(self.ChangePowerDialog.slider.value())
        
    def changeState(self):
        if self.on_button.isChecked(): # if button is checked
            self.on_button.setStyleSheet("background-color : lightblue") # setting background color to light-blue
            self.on_button.setText("On")
            self.parent.set_enabled(self._id, True)
        else: # if it is unchecked
            self.on_button.setStyleSheet("background-color : lightgrey") # set background color back to light-grey
            self.on_button.setText("Off")
            self.parent.set_enabled(self._id, False)

    def log_data(self, data):
        if (data.enabled):
            self.data_logger.log_data(data)
            
    def update_data(self, data):
        self.log_data(data)
        self.heating = data.heating
        if (self.sensor_id == 0): 
            self.power_dial.setValue(data.power)
        else:
            self.temperature=data.temperatur
            self.setpoint=data.setpoint
            self.temp_label.setText(f"{data.temperatur:.1f} °C")
            self.temp_label.repaint()  # Tvinger en opdatering af labelen
            self.sp_label.setText(f"(SP: {data.setpoint} °C)")
            self.sp_label.repaint()  # Tvinger en opdatering af labelen
            if (self.heating):
                self.statustext.setText(f"Varmer")
                self.statustext.setStyleSheet("font-size: 20px;background-color: yellow")
            else:
                self.statustext.setText(f"Varmer ikke")
                self.statustext.setStyleSheet("font-size: 20px;background-color: #e9e9e9;")
     
    def update_temperature(self, temperature, setpoint):
        self.temperature=temperature
        self.setpoint=setpoint
        # Opdater GUI'en med den modtagne temperatur
        self.temp_label.setText(f"{temperature:.1f} °C")
        self.temp_label.repaint()  # Tvinger en opdatering af labelen
        self.sp_label.setText(f"(SP: {setpoint} °C)")
        self.sp_label.repaint()  # Tvinger en opdatering af labelen
#        self.statustext.setEnabled(heating)

    def get_widget(self):
        return self.group_box
