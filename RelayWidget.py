from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QLineEdit, QSlider, QDialog, QGroupBox
import ChangeSetpointDialog

class RelayWidget(QWidget):
    def __init__(self, Relay_1_Name, Relay_2_Name, Relay_3_Name, Relay_4_Name):
        super().__init__()
        
        self.relay_1_label = QLabel(Relay_1_Name, self)
        self.relay_1_label.setAlignment(Qt.AlignCenter)
        self.relay_1_label.setStyleSheet("font-size: 30px;")

        self.relay_1_button = QPushButton("On", self)
        self.relay_1_button.setCheckable(True) # setting checkable to true
        self.relay_1_button.clicked.connect(self.relay_1_changeState) # setting calling method by button
        self.relay_1_button.setStyleSheet("background-color : lightblue") # setting default color of button to light-blue
        self.relay_1_button.setChecked(True)
        
        self.relay_2_label = QLabel(Relay_2_Name, self)
        self.relay_2_label.setAlignment(Qt.AlignCenter)
        self.relay_2_label.setStyleSheet("font-size: 30px;")

        self.relay_2_button = QPushButton("On", self)
        self.relay_2_button.setCheckable(True) # setting checkable to true
        self.relay_2_button.clicked.connect(self.relay_2_changeState) # setting calling method by button
        self.relay_2_button.setStyleSheet("background-color : lightblue") # setting default color of button to light-blue
        self.relay_2_button.setChecked(True)
        
        self.relay_3_label = QLabel(Relay_3_Name, self)
        self.relay_3_label.setAlignment(Qt.AlignCenter)
        self.relay_3_label.setStyleSheet("font-size: 30px;")

        self.relay_3_button = QPushButton("On", self)
        self.relay_3_button.setCheckable(True) # setting checkable to true
        self.relay_3_button.clicked.connect(self.relay_3_changeState) # setting calling method by button
        self.relay_3_button.setStyleSheet("background-color : lightblue") # setting default color of button to light-blue
        self.relay_3_button.setChecked(True)
        
        self.relay_4_label = QLabel(Relay_4_Name, self)
        self.relay_4_label.setAlignment(Qt.AlignCenter)
        self.relay_4_label.setStyleSheet("font-size: 30px;")

        self.relay_4_button = QPushButton("On", self)
        self.relay_4_button.setCheckable(True) # setting checkable to true
        self.relay_4_button.clicked.connect(self.relay_4_changeState) # setting calling method by button
        self.relay_4_button.setStyleSheet("background-color : lightblue") # setting default color of button to light-blue
        self.relay_4_button.setChecked(True)

        # Opret layout
        layout = QGridLayout()
        layout.addWidget(self.relay_1_label, 0, 0)
        layout.addWidget(self.relay_1_button, 1, 0)
        layout.addWidget(self.relay_2_label, 0, 1)
        layout.addWidget(self.relay_2_button, 1, 1)
        layout.addWidget(self.relay_3_label, 0, 2)
        layout.addWidget(self.relay_3_button, 1, 2)
        layout.addWidget(self.relay_4_label, 0, 3)
        layout.addWidget(self.relay_4_button, 1, 3)
        self.setLayout(layout)
    
    def relay_1_changeState(self):
        if self.relay_1_button.isChecked(): # if button is checked
            self.relay_1_button.setStyleSheet("background-color : lightblue") # setting background color to light-blue
            self.relay_1_button.setText("On")
        else: # if it is unchecked
            self.relay_1_button.setStyleSheet("background-color : lightgrey") # set background color back to light-grey
            self.relay_1_button.setText("Off")
    
    def relay_2_changeState(self):
        if self.relay_2_button.isChecked(): # if button is checked
            self.relay_2_button.setStyleSheet("background-color : lightblue") # setting background color to light-blue
            self.relay_2_button.setText("On")
        else: # if it is unchecked
            self.relay_2_button.setStyleSheet("background-color : lightgrey") # set background color back to light-grey
            self.relay_2_button.setText("Off")
    
    def relay_3_changeState(self):
        if self.relay_3_button.isChecked(): # if button is checked
            self.relay_3_button.setStyleSheet("background-color : lightblue") # setting background color to light-blue
            self.relay_3_button.setText("On")
        else: # if it is unchecked
            self.relay_3_button.setStyleSheet("background-color : lightgrey") # set background color back to light-grey
            self.relay_3_button.setText("Off")
    
    def relay_4_changeState(self):
        if self.relay_4_button.isChecked(): # if button is checked
            self.relay_4_button.setStyleSheet("background-color : lightblue") # setting background color to light-blue
            self.relay_4_button.setText("On")
        else: # if it is unchecked
            self.relay_4_button.setStyleSheet("background-color : lightgrey") # set background color back to light-grey
            self.relay_4_button.setText("Off")

    def get_widget(self):
        return self
