from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QLineEdit, QSlider, QDialog, QGroupBox

class TermostatWidget(QWidget):
    def __init__(self, title):
        super().__init__()
        
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

        # Opretter en gruppe til formområdet
        self.group_box = QGroupBox(title)

        # Opret layout
        layout = QGridLayout()
        layout.addWidget(self.header1,0,0)
        layout.addWidget(self.temp_label,1,0)
        layout.addWidget(self.sp_label,2,0)
        layout.addWidget(self.statustext,3,0)
        self.group_box.setLayout(layout)

    def update_temperature(self, temperature, setpoint, heating):
        # Opdater GUI'en med den modtagne temperatur
        self.temp_label.setText(temperature)
        self.sp_label.setText(setpoint)
        self.statustext.setEnabled(heating)

    def get_widget(self):
        return self.group_box
