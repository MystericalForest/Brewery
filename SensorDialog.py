import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QCheckBox, QRadioButton, QComboBox, QGridLayout, QLabel, QPushButton
from PyQt5.QtCore import QTimer, Qt, QSettings
import matplotlib
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)

class GraphForm(QMainWindow): #QWidget):
    def __init__(self, parent, data):
        super().__init__()
        
        self.parent = parent
        self.data = data

        # Opret UI komponenter
        self.init_ui()

    def init_ui(self):
        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        temperature, time = self.data.get_graph_data() #self.parent.parent.parent.parent.sensorData6.get_graph_data()
        sc.axes.plot(time, temperature)
        self.setCentralWidget(sc)

        self.show()
        
class SensorWidget(QWidget):
    def __init__(self, parent, name, sensor_id, data):
        super().__init__()
        self.parent = parent
        self.sensor_id = sensor_id
        self.sensor_type = "PT100"
        self.name = name
        self.data = data

        self.initUI()

    def initUI(self):
        # Opret widgets
        self.name_label = QLabel(self.name, self)
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setStyleSheet("font-size: 30px;")
        
        self.sensor_id_label = QLabel(f"Sensor: {self.sensor_id}")
#        self.sensor_id_label.setAlignment(Qt.AlignCenter)
        self.sensor_id_label.setStyleSheet("font-size: 18px;background-color: none")
        
        self.sensor_type_label = QLabel(f"Type: {self.sensor_type}")
#        self.sensor_type_label.setAlignment(Qt.AlignCenter)
        self.sensor_type_label.setStyleSheet("font-size: 18px;background-color: none")

        self.temp_label = QLabel("-- °C", self)
#        self.temp_label.setAlignment(Qt.AlignCenter)
        self.temp_label.setStyleSheet("font-size: 72px;background-color: none")
        
        self.error_label = QLabel(f"Error: Ok")
#        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setStyleSheet("font-size: 18px;background-color: none")
        
        self.graf_button = QPushButton("Graf")
        self.graf_button.clicked.connect(self.show_graph)

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
        self.sensor_type_label.setText(f"Type: {data.sensor_type}")
        if (data.errorflag == True):
            self.temp_label.setText(f"--- °C")
            self.temp_label.setStyleSheet("font-size: 72px;background-color: red")
            self.error_label.setStyleSheet("font-size: 18px;background-color: red")
            self.sensor_type_label.setStyleSheet("font-size: 18px;background-color: red")
            self.sensor_id_label.setStyleSheet("font-size: 18px;background-color: red")
        else:
            self.temp_label.setText(f"{data.temperature:.1f} °C")
            self.temp_label.setStyleSheet("font-size: 72px;background-color: none")
            self.error_label.setStyleSheet("font-size: 18px;background-color: none")
            self.sensor_type_label.setStyleSheet("font-size: 18px;background-color: none")
            self.sensor_id_label.setStyleSheet("font-size: 18px;background-color: none")
        self.error_label.setText(f"Error: {data.errorDescription}")
        self.sensor_type_label.repaint()
        self.temp_label.repaint()
        self.error_label.repaint()

    def show_graph(self):
        pass
        # Åbner grafen i nyt vindue
        self.graphForm = GraphForm(self, self.data)
        self.graphForm.show()
    
    def get_widget(self):
        return self
        
class SensorDialog(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        # Opret UI komponenter
        self.init_ui()
        
        self.load_settings()
        
        # Opret en timer
        if (not self.parent.parent.demo_mode):
            timer = QTimer(self, interval=2000, timeout=self.update_data)
            timer.start()

    def init_ui(self):
        # Opret widgets
        self.sensor1 = SensorWidget(self, "PT100 transmitter #1", 1, self.parent.parent.sensorData1)
        self.sensor2 = SensorWidget(self, "PT100 transmitter #2", 2, self.parent.parent.sensorData2)
        self.sensor3 = SensorWidget(self, "PT100 transmitter #3", 3, self.parent.parent.sensorData3)
        self.sensor4 = SensorWidget(self, "PT100 transmitter #4", 4, self.parent.parent.sensorData4)
        self.sensor5 = SensorWidget(self, "D18BS20 transmitter #1", 5, self.parent.parent.sensorData5)
        self.sensor6 = SensorWidget(self, "D18BS20 transmitter #2", 6, self.parent.parent.sensorData6)
        
        # OK og Cancel knapper
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")
        
        # Layout
        self.layout = QGridLayout()
        
        # Tilføj widgets til layoutet
        self.layout.addWidget(self.sensor1.get_widget(), 0, 0)
        self.layout.addWidget(self.sensor2.get_widget(), 0, 1)
        self.layout.addWidget(self.sensor3.get_widget(), 0, 2)
        self.layout.addWidget(self.sensor4.get_widget(), 1, 0)
        self.layout.addWidget(self.sensor5.get_widget(), 1, 1)
        self.layout.addWidget(self.sensor6.get_widget(), 1, 2)
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
    
    def update_data(self):
        self.sensor1.update_data(self.parent.parent.sensorData1.last_datapoint)
        self.sensor2.update_data(self.parent.parent.sensorData2.last_datapoint)
        self.sensor3.update_data(self.parent.parent.sensorData3.last_datapoint)
        self.sensor4.update_data(self.parent.parent.sensorData4.last_datapoint)
        self.sensor5.update_data(self.parent.parent.sensorData5.last_datapoint)
        self.sensor6.update_data(self.parent.parent.sensorData6.last_datapoint)
    
    def on_ok(self):
        self.close()  # Luk vinduet efter OK

    def on_cancel(self):
        self.close()  # Luk vinduet efter Cancel
