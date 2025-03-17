from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QLineEdit, QSlider, QDialog

class ChangeSetpointDialog(QDialog):
    
    # Definerer et signal, der sender værdierne tilbage til hovedvinduet
    values_transferred = pyqtSignal(int)
        
    def __init__(self, name, setpoint1):
        super().__init__()

        # Opsætning af det nye vindue
        self.setWindowTitle("Ret setpunkter")
        self.setGeometry(200, 200, 300, 200)

        # Layout og inputfelter
        layout = QGridLayout()
        
        # Slider 1
        self.label = QLabel("Setpoint for " + name, self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 30px;")
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setRange(0, 100)  # Sætter intervallet for slideren
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(10)
        self.slider.setValue(setpoint1) 
        self.slider.valueChanged.connect(self.update_value)
        self.value = QLabel(f"{setpoint1} °C", self)
        self.value.setAlignment(Qt.AlignCenter)
        self.value.setStyleSheet("font-size: 48px;")
        layout.addWidget(self.label,0,0, 1, 2)
        layout.addWidget(self.value,1,0, 1, 2)
        layout.addWidget(self.slider,2,0, 1, 2)

        self.ok_button = QPushButton('Ok', self)
        self.ok_button.clicked.connect(self.ok_clicked)
        layout.addWidget(self.ok_button,3,0)
 
        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.cancel_clicked)
        layout.addWidget(self.cancel_button,3,1)

        self.setLayout(layout)

    def update_value(self):
        self.value.setText(f"{self.slider.value()} °C")
        
    def ok_clicked(self):
        # Sender værdierne tilbage til hovedvinduet via signal
        self.values_transferred.emit(self.slider.value())
        self.accept()  # Lukker dialogen efter overførsel

    def cancel_clicked(self):
        pass
