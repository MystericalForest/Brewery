from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QLineEdit, QSlider, QDialog, QGroupBox
import ChangeSetpointDialog

class RelayWidget(QWidget):
    def __init__(self, parent, Relay_1_Name, Relay_2_Name, Relay_3_Name, Relay_4_Name):
        super().__init__()
        self.parent=parent
        
        self.relay_1_label = QLabel(Relay_1_Name, self)
        self.relay_1_label.setAlignment(Qt.AlignRight)
        self.relay_1_label.setStyleSheet("font-size: 30px;")

        self.relay_1_button = QPushButton("Off", self)
        self.relay_1_button.setCheckable(True) # setting checkable to true
        self.relay_1_button.clicked.connect(self.relay_1_changeState) # setting calling method by button
        self.relay_1_button.setStyleSheet("background-color : lightgrey") # setting default color of button to light-gray
        self.relay_1_button.setFixedSize(100,50) 
        self.relay_1_button.setChecked(False)
        
        self.relay_2_label = QLabel(Relay_2_Name, self)
        self.relay_2_label.setAlignment(Qt.AlignRight)
        self.relay_2_label.setStyleSheet("font-size: 30px;")

        self.relay_2_button = QPushButton("Off", self)
        self.relay_2_button.setCheckable(True) # setting checkable to true
        self.relay_2_button.clicked.connect(self.relay_2_changeState) # setting calling method by button
        self.relay_2_button.setStyleSheet("background-color : lightgrey") # setting default color of button to light-gray
        self.relay_2_button.setFixedSize(100,50)
        self.relay_2_button.setChecked(False)
        
        self.relay_3_label = QLabel(Relay_3_Name, self)
        self.relay_3_label.setAlignment(Qt.AlignRight)
        self.relay_3_label.setStyleSheet("font-size: 30px;")

        self.relay_3_button = QPushButton("Off", self)
        self.relay_3_button.setCheckable(True) # setting checkable to true
        self.relay_3_button.clicked.connect(self.relay_3_changeState) # setting calling method by button
        self.relay_3_button.setStyleSheet("background-color : lightgrey") # setting default color of button to light-gray
        self.relay_3_button.setFixedSize(100,50)
        self.relay_3_button.setChecked(False)
        
        self.relay_4_label = QLabel(Relay_4_Name, self)
        self.relay_4_label.setAlignment(Qt.AlignRight)
        self.relay_4_label.setStyleSheet("font-size: 30px;")

        self.relay_4_button = QPushButton("Off", self)
        self.relay_4_button.setCheckable(True) # setting checkable to true
        self.relay_4_button.clicked.connect(self.relay_4_changeState) # setting calling method by button
        self.relay_4_button.setStyleSheet("background-color : lightgrey") # setting default color of button to light-gray
        self.relay_4_button.setFixedSize(100,50)
        self.relay_4_button.setChecked(False)

        # Opret layout
        layout = QGridLayout()
        layout.addWidget(self.relay_1_label, 0, 0)
        layout.addWidget(self.relay_1_button, 0, 1)
        layout.addWidget(self.relay_2_label, 1, 0)
        layout.addWidget(self.relay_2_button, 1, 1)
        layout.addWidget(self.relay_3_label, 2, 0)
        layout.addWidget(self.relay_3_button, 2, 1)
        layout.addWidget(self.relay_4_label, 3, 0)
        layout.addWidget(self.relay_4_button, 3, 1)
        self.setLayout(layout)
    
    def relay_1_changeState(self):
        if self.relay_1_button.isChecked(): # if button is checked
            self.relay_1_button.setStyleSheet("background-color : lightblue") # setting background color to light-blue
            self.relay_1_button.setText("On")
            self.parent.set_relay_1(True)
        else: # if it is unchecked
            self.relay_1_button.setStyleSheet("background-color : lightgrey") # set background color back to light-grey
            self.relay_1_button.setText("Off")
            self.parent.set_relay_1(False)
    
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
