from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QLineEdit, QSlider, QDialog, QGroupBox
from PyQt5.QtGui import QIcon
import SettingsDialog, SensorDialog

class ButtonsWidget(QWidget):
    def __init__(self, parent, title):
        super().__init__()
 
        self.parent = parent
        self.settings_button = QPushButton('', self)
        self.settings_button.clicked.connect(self.open_setting_dialog)
        self.settings_button.setIcon(QIcon('settings-icon.jpg'))
        self.settings_button.setIconSize(QSize(90, 90))
        self.settings_button.setFixedSize(100,100)
        
        self.sensors_button = QPushButton('', self)
        self.sensors_button.clicked.connect(self.open_sensor_dialog)
        self.sensors_button.setIcon(QIcon('temperature-icon.png'))
        self.sensors_button.setIconSize(QSize(90, 90))
        self.sensors_button.setFixedSize(100,100)

        # Opretter en gruppe til formområdet
        self.group_box = QGroupBox(title)

        # Opret layout
        layout = QGridLayout()
        layout.addWidget(self.settings_button,1,0)
        layout.addWidget(self.sensors_button,1,1)
        self.group_box.setLayout(layout)

    def open_setting_dialog(self):
        # Åbner det nye vindue
        self.SettingsDialog = SettingsDialog.SettingsDialog(self)
        self.SettingsDialog.show()
#        if self.SettingsDialog.exec_()  == QDialog.Accepted:
#            print("Settings Accepted")

    def open_sensor_dialog(self):
        # Åbner det nye vindue
        self.SensorDialog = SensorDialog.SensorDialog(self)
        self.SensorDialog.show()

    def get_widget(self):
        return self.group_box
