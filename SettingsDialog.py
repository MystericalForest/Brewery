import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QCheckBox, QRadioButton, QGridLayout, QLabel, QPushButton
from PyQt5.QtCore import QSettings

class SettingsDialog(QWidget):
    def __init__(self):
        super().__init__()

        # Opret QSettings objektet
        self.settings = QSettings("VestervangBryglaug", "BrewControl")

        # Opret UI komponenter
        self.init_ui()
        
        self.load_settings()

    def init_ui(self):
        # Opret widgets
        self.port_label = QLabel("COM Port:")
        self.termo_1_name_label = QLabel("Termostat 1:")
        self.termo_2_name_label = QLabel("Termostat 2:")
        self.termo_3_name_label = QLabel("Termostat 3:")
        self.watch_1_name_label = QLabel("Ur 1 navn:")
        self.watch_2_name_label = QLabel("Ur 2 navn:")
        self.watch_3_name_label = QLabel("Ur 3 navn:")
        self.port_input = QLineEdit()
        self.termo_1_name_input = QLineEdit()
        self.termo_2_name_input = QLineEdit()
        self.termo_3_name_input = QLineEdit()
        self.watch_1_name_input = QLineEdit()
        self.watch_2_name_input = QLineEdit()
        self.watch_3_name_input = QLineEdit()
        self.demo_mode_checkbox = QCheckBox("Demo mode")
        self.radio_button1 = QRadioButton("Option 1")
        self.radio_button2 = QRadioButton("Option 2")
        
        # OK og Cancel knapper
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")
        
        # Layout
        self.layout = QGridLayout()
        
        # Tilføj widgets til layoutet
        self.layout.addWidget(self.port_label, 0, 0)
        self.layout.addWidget(self.demo_mode_checkbox, 0, 2)
        self.layout.addWidget(self.port_input, 0, 1)
        self.layout.addWidget(self.termo_1_name_label, 1, 0)
        self.layout.addWidget(self.termo_1_name_input, 1, 1, 1, 2)
        self.layout.addWidget(self.termo_2_name_label, 2, 0)
        self.layout.addWidget(self.termo_2_name_input, 2, 1, 1, 2)
        self.layout.addWidget(self.termo_3_name_label, 3, 0)
        self.layout.addWidget(self.termo_3_name_input, 3, 1, 1, 2)
        self.layout.addWidget(self.watch_1_name_label, 4, 0)
        self.layout.addWidget(self.watch_1_name_input, 4, 1, 1, 2)
        self.layout.addWidget(self.watch_2_name_label, 5, 0)
        self.layout.addWidget(self.watch_2_name_input, 5, 1, 1, 2)
        self.layout.addWidget(self.watch_3_name_label, 6, 0)
        self.layout.addWidget(self.watch_3_name_input, 6, 1, 1, 2)
        self.layout.addWidget(self.radio_button1, 7, 0)
        self.layout.addWidget(self.radio_button2, 7, 1)
        self.layout.addWidget(self.ok_button, 8, 0)
        self.layout.addWidget(self.cancel_button, 8, 1, 1, 2)
        
        # Sæt layout
        self.setLayout(self.layout)
        
        # Vinduestitel
        self.setWindowTitle("Indstillinger")
        
        # Forbind knapperne med funktioner
        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)

    def load_settings(self):
        self.port_input.setText(self.settings.value("port", ""))
        self.termo_1_name_input.setText(self.settings.value("termo_1_name", ""))
        self.termo_2_name_input.setText(self.settings.value("termo_2_name", ""))
        self.termo_3_name_input.setText(self.settings.value("termo_3_name", ""))
        self.watch_1_name_input.setText(self.settings.value("watch_1_name", ""))
        self.watch_2_name_input.setText(self.settings.value("watch_2_name", ""))
        self.watch_3_name_input.setText(self.settings.value("watch_3_name", ""))
        self.demo_mode_checkbox.setChecked(self.settings.value("demo_mode", False, type=bool))
    
    def on_ok(self):
        self.settings.setValue("port", self.port_input.text())
        self.settings.setValue("termo_1_name", self.termo_1_name_input.text())
        self.settings.setValue("termo_2_name", self.termo_2_name_input.text())
        self.settings.setValue("termo_3_name", self.termo_3_name_input.text())
        self.settings.setValue("watch_1_name", self.watch_1_name_input.text())
        self.settings.setValue("watch_2_name", self.watch_2_name_input.text())
        self.settings.setValue("watch_3_name", self.watch_3_name_input.text())
        self.settings.setValue("demo_mode", self.demo_mode_checkbox.isChecked())
        # Håndter OK knap klik
        print("OK button clicked!")
        print(f"Port: {self.port_input.text()}")
        print(f"Demo mode: {self.demo_mode_checkbox.isChecked()}")
        print(f"Selected option: {'Option 1' if self.radio_button1.isChecked() else 'Option 2' if self.radio_button2.isChecked() else 'None'}")
        self.close()  # Luk vinduet efter OK

    def on_cancel(self):
        # Håndter Cancel knap klik
        print("Cancel button clicked!")
        self.close()  # Luk vinduet efter Cancel
