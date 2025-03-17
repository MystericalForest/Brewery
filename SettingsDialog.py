from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QLineEdit, QSlider, QDialog

class SettingsDialog(QDialog):
    
    # Definerer et signal, der sender værdierne tilbage til hovedvinduet
 #   values_transferred = pyqtSignal(int, int, int)
        
    def __init__(self):
        super().__init__()

        # Opsætning af det nye vindue
        self.setWindowTitle("Opsætning")
        self.setGeometry(200, 200, 300, 200)

        # Layout og inputfelter
        layout = QGridLayout()
        
        # Slider 1
        self.label1 = QLabel("Setpoint 1:", self)

        self.setLayout(layout)
        
    def ok_clicked(self):
        pass

    def cancel_clicked(self):
        pass
