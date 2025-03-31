from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QDial, QLineEdit, QSlider, QDialog, QGroupBox
import ChangeSetpointDialog, SettingsDialog

class TermoData():
    def __init__(self):
        self.temperature=0
        self.setpoint=0
        self.heating=False

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
    # Opretter et signal, der sender dataene
    temperature_updated = pyqtSignal(int, int)  # Temperatur, Setpoint, Heating Status

    def __init__(self, title, sensor_id):
        super().__init__()
        self.title = title
        self.sensor_id = sensor_id
        
        self.on_button = QPushButton("On", self)
        self.on_button.setCheckable(True) # setting checkable to true
        self.on_button.clicked.connect(self.changeState) # setting calling method by button
        self.on_button.setStyleSheet("background-color : lightblue") # setting default color of button to light-blue
        self.on_button.setChecked(True)
        
        self.header1 = QLabel(title, self)
        self.header1.setAlignment(Qt.AlignCenter)
        self.header1.setStyleSheet("font-size: 30px;")
        
        self.temp_label = QLabel("-- °C", self)
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.temp_label.setStyleSheet("font-size: 72px;")
        
        self.sp_label = QLabel("(SP: -- °C)", self)
        self.sp_label.setAlignment(Qt.AlignCenter)
        self.sp_label.setStyleSheet("font-size: 30px;")
        
        self.statustext = QLabel("Varmer", self)
        self.statustext.setAlignment(Qt.AlignCenter)
        self.statustext.setStyleSheet("font-size: 20px;background-color: yellow")
        self.statustext.setEnabled(True)
        
        self.setpoint_button = QPushButton("Ret Setpoint", self)
        self.setpoint_button.clicked.connect(self.open_setpoint_dialog) # setting calling method by button
        
        self.power_dial = QDial(self)
        self.power_dial.setRange(0, 100)
        self.power_dial.setValue(50)
        
        self.power_label = QLabel("50 %", self)
        self.power_label.setAlignment(Qt.AlignCenter)
        self.power_label.setStyleSheet("font-size: 30px;")

        # Forbinder signalet til ændring af værdien med en slot (metode)
        self.power_dial.valueChanged.connect(self.updateLabel)
 
        # Opretter en gruppe til formområdet
        self.group_box = QGroupBox(title)

        # Opret layout
        layout = QGridLayout()
        layout.addWidget(self.on_button,0,0)
        layout.addWidget(self.header1,1,0)
        if (self.sensor_id == 0):
            layout.addWidget(self.power_dial, 2, 0)
            layout.addWidget(self.power_label, 3, 0)
        else:
            layout.addWidget(self.temp_label,2,0)
            layout.addWidget(self.sp_label,3,0)
            layout.addWidget(self.statustext,4,0)
            layout.addWidget(self.setpoint_button,5,0)
        self.group_box.setLayout(layout)

        # Forbinder signalet til slotten
        self.temperature_updated.connect(self.update_temperature)

    def updateLabel(self):
        # Opdaterer labelen med den aktuelle værdi fra drejeknappen
        self.power_label.setText(f"{self.power_dial.value()} %")
        
    def open_setpoint_dialog(self):
        # Åbner det nye vindue
        self.ChangeSetpointDialog = ChangeSetpointDialog.ChangeSetpointDialog(self.title, 50)
        if self.ChangeSetpointDialog.exec_()  == QDialog.Accepted:
            self.update_temperature(50,self.ChangeSetpointDialog.slider.value())
        
    def changeState(self):
        if self.on_button.isChecked(): # if button is checked
            self.on_button.setStyleSheet("background-color : lightblue") # setting background color to light-blue
            self.on_button.setText("On")
        else: # if it is unchecked
            self.on_button.setStyleSheet("background-color : lightgrey") # set background color back to light-grey
            self.on_button.setText("Off")
 
    def update_temperature(self, temperature, setpoint):
        # Opdater GUI'en med den modtagne temperatur
        self.temp_label.setText(f"{temperature} °C")
        self.temp_label.repaint()  # Tvinger en opdatering af labelen
        self.sp_label.setText(f"(SP: {setpoint} °C)")
        self.sp_label.repaint()  # Tvinger en opdatering af labelen
#        self.statustext.setEnabled(heating)

    def get_widget(self):
        return self.group_box
