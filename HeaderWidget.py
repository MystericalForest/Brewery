from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QLineEdit, QSlider, QDialog, QGroupBox

class HeaderWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.header = QLabel("BrewControl", self)
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setStyleSheet("font-size: 30px;")
        
        self.status_label = QLabel("Advarsel: Temperatur er lav!", self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 18px;")

        # Opret layout
        layout = QGridLayout()
        layout.addWidget(self.header,0,0)
        layout.addWidget(self.status_label,1,0)

        self.setLayout(layout)

    def get_widget(self):
        return self
