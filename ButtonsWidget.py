from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QLineEdit, QSlider, QDialog, QGroupBox
import SettingsDialog

class ButtonsWidget(QWidget):
    def __init__(self, title):
        super().__init__()
 
        self.settings_button = QPushButton('Settings', self)
        self.settings_button.clicked.connect(self.open_setting_dialog)
        self.settings_button.setFixedSize(100,50)

        # Opretter en gruppe til formområdet
        self.group_box = QGroupBox(title)

        # Opret layout
        layout = QGridLayout()
        layout.addWidget(self.settings_button,1,0)
        self.group_box.setLayout(layout)

    def open_setting_dialog(self):
        # Åbner det nye vindue
        self.SettingsDialog = SettingsDialog.SettingsDialog()
        self.SettingsDialog.show()

    def get_widget(self):
        return self.group_box
