import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QCheckBox, QRadioButton, QComboBox, QGridLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, QSettings

class SensorWidget(QWidget):
    def __init__(self, parent, name, sensor_id):
        super().__init__()
        self.parent = parent
        self.sensor_id = sensor_id
        self.sensor_type = "PT100"
        self.name = name

        self.initUI()

    def initUI(self):
        # Opret widgets
        self.name_label = QLabel(self.name, self)
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setStyleSheet("font-size: 30px;")
        
        self.sensor_id_label = QLabel(f"Sensor: {self.sensor_id}")
#        self.sensor_id_label.setAlignment(Qt.AlignCenter)
        self.sensor_id_label.setStyleSheet("font-size: 18px;")
        
        self.sensor_type_label = QLabel(f"Type: {self.sensor_type}")
#        self.sensor_type_label.setAlignment(Qt.AlignCenter)
        self.sensor_type_label.setStyleSheet("font-size: 18px;")

        self.temp_label = QLabel("-- °C", self)
#        self.temp_label.setAlignment(Qt.AlignCenter)
        self.temp_label.setStyleSheet("font-size: 72px;")
        
        self.error_label = QLabel(f"Error: Ok")
#        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setStyleSheet("font-size: 18px;")
        
        self.graf_button = QPushButton("Graf")

        # Opret layout
        self.layout = QGridLayout()
        self.layout.addWidget(self.name_label, 0, 0, 1, 2)
        self.layout.addWidget(self.sensor_id_label, 1, 0)
        self.layout.addWidget(self.sensor_type_label, 1, 1)
        self.layout.addWidget(self.temp_label, 2, 0, 1, 2)
        self.layout.addWidget(self.error_label, 3, 0, 1, 2)
        self.layout.addWidget(self.graf_button, 4, 0, 1, 2)
        
        # Sæt layout
        self.setLayout(self.layout)
            
    def update_data(self, data):
        pass
#        self.temp_label.setText(f"{data.temperatur:.1f} °C")
#        self.temp_label.repaint()  # Tvinger en opdatering af labelen

    def get_widget(self):
        return self
        
class SensorDialog(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        # Opret UI komponenter
        self.init_ui()
        
        self.load_settings()

    def init_ui(self):
        # Opret widgets
        self.sensor1 = SensorWidget(self, "PT100 transmitter #1", 1)
        self.sensor2 = SensorWidget(self, "PT100 transmitter #2", 2)
        self.sensor3 = SensorWidget(self, "PT100 transmitter #3", 3)
        self.sensor4 = SensorWidget(self, "PT100 transmitter #4", 4)
        self.sensor5 = SensorWidget(self, "D18BS20 transmitter #1", 5)
        self.sensor6 = SensorWidget(self, "D18BS20 transmitter #2", 6)
        
        # OK og Cancel knapper
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")
        
        # Layout
        self.layout = QGridLayout()
        
        # Tilføj widgets til layoutet
        self.layout.addWidget(self.sensor1.get_widget(), 0, 0)
        self.layout.addWidget(self.sensor2.get_widget(), 0, 1)
        self.layout.addWidget(self.sensor3.get_widget(), 1, 0)
        self.layout.addWidget(self.sensor4.get_widget(), 1, 1)
        self.layout.addWidget(self.sensor5.get_widget(), 2, 0)
        self.layout.addWidget(self.sensor6.get_widget(), 2, 1)
        self.layout.addWidget(self.ok_button, 3, 0)
        self.layout.addWidget(self.cancel_button, 3, 1)
        
        # Sæt layout
        self.setLayout(self.layout)
        
        # Vinduestitel
        self.setWindowTitle("Sensor")
        
        # Forbind knapperne med funktioner
        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)

    def load_settings(self):
        pass
    
    def on_ok(self):
        self.close()  # Luk vinduet efter OK

    def on_cancel(self):
        self.close()  # Luk vinduet efter Cancel
