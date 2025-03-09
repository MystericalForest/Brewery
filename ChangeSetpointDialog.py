from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QLineEdit, QSlider, QDialog

class ChangeSetpointDialog(QDialog):
    
    # Definerer et signal, der sender værdierne tilbage til hovedvinduet
    values_transferred = pyqtSignal(int, int, int)
        
    def __init__(self, setpoint1, setpoint2, setpoint3):
        super().__init__()

        # Opsætning af det nye vindue
        self.setWindowTitle("Ret setpunkter")
        self.setGeometry(200, 200, 300, 200)

        # Layout og inputfelter
        layout = QGridLayout()
        
        # Slider 1
        self.label1 = QLabel("Setpoint 1:", self)
        self.slider1 = QSlider(Qt.Horizontal, self)
        self.slider1.setRange(0, 100)  # Sætter intervallet for slideren
        self.slider1.setTickPosition(QSlider.TicksBelow)
        self.slider1.setTickInterval(10)
        self.slider1.setValue(setpoint1) 
        self.slider1.valueChanged.connect(self.update_value1)
        self.value1 = QLabel(str(setpoint1), self)
        layout.addWidget(self.label1,0,0)
        layout.addWidget(self.slider1,1,0)
        layout.addWidget(self.value1,1,1)

        # Slider 2
        self.label2 = QLabel("Setpoint 2:", self)
        self.slider2 = QSlider(Qt.Horizontal, self)
        self.slider2.setRange(0, 100)
        self.slider2.setTickPosition(QSlider.TicksBelow)
        self.slider2.setTickInterval(10)
        self.slider2.setValue(setpoint2) 
        self.slider2.valueChanged.connect(self.update_value2)
        self.value2 = QLabel(str(setpoint2), self)
        layout.addWidget(self.label2,2,0)
        layout.addWidget(self.slider2,3,0)
        layout.addWidget(self.value2,3,1)

        # Slider 3
        self.label3 = QLabel("Setpoint 3:", self)
        self.slider3 = QSlider(Qt.Horizontal, self)
        self.slider3.setRange(0, 100)
        self.slider3.setTickPosition(QSlider.TicksBelow)
        self.slider3.setTickInterval(10)
        self.slider3.setValue(setpoint3) 
        self.slider3.valueChanged.connect(self.update_value3)
        self.value3 = QLabel(str(setpoint3), self)
        layout.addWidget(self.label3,4,0)
        layout.addWidget(self.slider3,5,0)
        layout.addWidget(self.value3,5,1)

        self.ok_button = QPushButton('Ok', self)
        self.ok_button.clicked.connect(self.ok_clicked)
        layout.addWidget(self.ok_button,6,0)
 
        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.cancel_clicked)
        layout.addWidget(self.cancel_button,6,1)

        self.setLayout(layout)

    def update_value1(self):
        self.value1.setText(f"{self.slider1.value()}")

    def update_value2(self):
        self.value2.setText(f"{self.slider2.value()}")

    def update_value3(self):
        self.value3.setText(f"{self.slider3.value()}")
        
    def ok_clicked(self):
        # Sender værdierne tilbage til hovedvinduet via signal
        self.values_transferred.emit(self.slider1.value(), self.slider2.value(), self.slider3.value())
        self.accept()  # Lukker dialogen efter overførsel

    def cancel_clicked(self):
        pass
