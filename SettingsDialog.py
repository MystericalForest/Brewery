import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QCheckBox, QRadioButton, QComboBox, QGridLayout, QLabel, QPushButton, QMessageBox 
from PyQt5.QtCore import QSettings

class PIDSettingsWindow(QWidget):
    def __init__(self, parent, termostat_id):
        self.parent = parent
        self.termostat_id = termostat_id
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("PID Opsætning (Termostat " + str(self.termostat_id) +")")

        # Labels og inputfelter
        
        
        # Fill combo with sensor names
        self.termo_sensor_label = QLabel("Termo Sensor:")
        self.termo_sensor_combo = QComboBox(self)
        
        self.termo_sensor_combo.addItem("Ingen")
        self.termo_sensor_combo.addItem("PT100 transmitter #1")
        self.termo_sensor_combo.addItem("PT100 transmitter #2")
        self.termo_sensor_combo.addItem("PT100 transmitter #3")
        self.termo_sensor_combo.addItem("PT100 transmitter #4")
        self.termo_sensor_combo.addItem("D18BS20 transmitter #1")
        self.termo_sensor_combo.addItem("D18BS20 transmitter #2")
        
        self.termo_type_label = QLabel("Termo Type:")
        self.termo_type_combo = QComboBox(self)
        
        self.termo_type_combo.addItem("Manuel")
        self.termo_type_combo.addItem("Simple")
        self.termo_type_combo.addItem("PID")
     #   self.termo_type_combo.addItem("Fuzzy Logic")
     #   self.termo_type_combo.addItem("Adaptiv/MPC")
        
        self.hyst_label = QLabel("Hysterese:")
        self.hyst_input = QLineEdit()
        
        self.kp_label = QLabel("Kp:")
        self.kp_input = QLineEdit()

        self.ki_label = QLabel("Ki:")
        self.ki_input = QLineEdit()

        self.kd_label = QLabel("Kd:")
        self.kd_input = QLineEdit()

        # Knap
        self.submit_btn = QPushButton("Anvend")
        self.submit_btn.clicked.connect(self.apply_settings)
        self.close_btn = QPushButton("Luk")
        self.close_btn.clicked.connect(self.close_window)

        # Layout
        grid_layout = QGridLayout()

        # Placer elementer i gitteret
        grid_layout.addWidget(self.termo_sensor_label, 0, 0)
        grid_layout.addWidget(self.termo_sensor_combo, 0, 1, 1, 3)
        
        grid_layout.addWidget(self.termo_type_label, 1, 0)
        grid_layout.addWidget(self.termo_type_combo, 1, 1, 1, 3)
        
        grid_layout.addWidget(self.kp_label, 2, 0)
        grid_layout.addWidget(self.kp_input, 2, 1)
        
        grid_layout.addWidget(self.hyst_label, 2, 2)
        grid_layout.addWidget(self.hyst_input, 2, 3)

        grid_layout.addWidget(self.ki_label, 3, 0)
        grid_layout.addWidget(self.ki_input, 3, 1)

        grid_layout.addWidget(self.kd_label, 3, 2)
        grid_layout.addWidget(self.kd_input, 3, 3)

        grid_layout.addWidget(self.submit_btn, 4, 0, 1, 2)
        grid_layout.addWidget(self.close_btn, 4, 2, 1, 2)

        self.setLayout(grid_layout)

        self.update_data()

    def update_data(self):
        kp, ki, kd = self.parent.parent.parent.get_termostat_settings(self.termostat_id)
        self.kp_input.setText(str(kp))
        self.ki_input.setText(str(ki))
        self.kd_input.setText(str(kd))

    def apply_settings(self):
        try:
            kp = float(self.kp_input.text())
            ki = float(self.ki_input.text())
            kd = float(self.kd_input.text())
            hysteresis = float(self.hyst_input.text())

            QMessageBox.information(self, "PID Parametre", f"Kp: {kp}\nKi: {ki}\nKd: {kd}\nHysterese: {hysteresis}")

            self.parent.parent.parent.update_termostat_settings(self.termostat_id, kp, ki, kd, hysteresis)
            
            # Her kan du sende værdierne videre til din PID-kontrol
            # fx self.pid.setTunings(kp, ki, kd)

        except ValueError:
            QMessageBox.warning(self, "Fejl", "Ugyldig indtastning! Brug kun tal.")

    def close_window(self):
        # Håndter Luk knap klik
        self.close()
            
class SettingsDialog(QWidget):
    def __init__(self, parent):
        super().__init__()

        # Opret QSettings objektet
        self.settings = QSettings("VestervangBryglaug", "BrewControl")
        self.parent = parent

        # Opret UI komponenter
        self.init_ui()
        
        self.load_settings()

    def init_ui(self):
        # Opret widgets
        self.port_label = QLabel("COM Port:")
        self.termo_1_name_label = QLabel("Termostat 1:")
        self.termo_1_sensor_label = QLabel("Termo Sensor:")
        self.termo_1_settings_button = QPushButton("Parametre")
        self.termo_2_name_label = QLabel("Termostat 2:")
        self.termo_2_sensor_label = QLabel("Termo Sensor:")
        self.termo_2_settings_button = QPushButton("Parametre")
        self.termo_3_name_label = QLabel("Termostat 3:")
        self.termo_3_sensor_label = QLabel("Termo Sensor:")
        self.termo_3_settings_button = QPushButton("Parametre")
        self.watch_1_name_label = QLabel("Ur 1 navn:")
        self.watch_2_name_label = QLabel("Ur 2 navn:")
        self.watch_3_name_label = QLabel("Ur 3 navn:")
        self.port_input = QLineEdit()
        self.termo_1_name_input = QLineEdit()
        self.termo_1_sensor_combo = QComboBox(self)
        self.termo_2_sensor_combo = QComboBox(self)
        self.termo_3_sensor_combo = QComboBox(self)
        self.termo_2_name_input = QLineEdit()
        self.termo_3_name_input = QLineEdit()
        self.watch_1_name_input = QLineEdit()
        self.watch_2_name_input = QLineEdit()
        self.watch_3_name_input = QLineEdit()
        self.demo_mode_checkbox = QCheckBox("Demo mode")
        
        # OK og Cancel knapper
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")
        
        # Fill combo with sensor names
        self.termo_1_sensor_combo.addItem("Manuel")
        self.termo_1_sensor_combo.addItem("PT100 transmitter #1")
        self.termo_1_sensor_combo.addItem("PT100 transmitter #2")
        self.termo_1_sensor_combo.addItem("PT100 transmitter #3")
        self.termo_1_sensor_combo.addItem("PT100 transmitter #4")
        self.termo_1_sensor_combo.addItem("D18BS20 transmitter #1")
        self.termo_1_sensor_combo.addItem("D18BS20 transmitter #2")
        
        self.termo_2_sensor_combo.addItem("Manuel")
        self.termo_2_sensor_combo.addItem("PT100 transmitter #1")
        self.termo_2_sensor_combo.addItem("PT100 transmitter #2")
        self.termo_2_sensor_combo.addItem("PT100 transmitter #3")
        self.termo_2_sensor_combo.addItem("PT100 transmitter #4")
        self.termo_2_sensor_combo.addItem("D18BS20 transmitter #1")
        self.termo_2_sensor_combo.addItem("D18BS20 transmitter #2")
        
        self.termo_3_sensor_combo.addItem("Manuel")
        self.termo_3_sensor_combo.addItem("PT100 transmitter #1")
        self.termo_3_sensor_combo.addItem("PT100 transmitter #2")
        self.termo_3_sensor_combo.addItem("PT100 transmitter #3")
        self.termo_3_sensor_combo.addItem("PT100 transmitter #4")
        self.termo_3_sensor_combo.addItem("D18BS20 transmitter #1")
        self.termo_3_sensor_combo.addItem("D18BS20 transmitter #2")
        
        # Layout
        self.layout = QGridLayout()
        
        # Tilføj widgets til layoutet
        self.layout.addWidget(self.port_label, 0, 0)
        self.layout.addWidget(self.demo_mode_checkbox, 0, 2)
        self.layout.addWidget(self.port_input, 0, 1)
        self.layout.addWidget(self.termo_1_name_label, 1, 0)
        self.layout.addWidget(self.termo_1_name_input, 1, 1)
        self.layout.addWidget(self.termo_1_settings_button, 1, 2)
        self.layout.addWidget(self.termo_1_sensor_label, 2, 0)
        self.layout.addWidget(self.termo_1_sensor_combo, 2, 1, 1, 2)
        self.layout.addWidget(self.termo_2_name_label, 3, 0)
        self.layout.addWidget(self.termo_2_name_input, 3, 1)
        self.layout.addWidget(self.termo_2_settings_button, 3, 2)
        self.layout.addWidget(self.termo_2_sensor_label, 4, 0)
        self.layout.addWidget(self.termo_2_sensor_combo, 4, 1, 1, 2)
        self.layout.addWidget(self.termo_3_name_label, 5, 0)
        self.layout.addWidget(self.termo_3_name_input, 5, 1)
        self.layout.addWidget(self.termo_3_settings_button, 5, 2)
        self.layout.addWidget(self.termo_3_sensor_label, 6, 0)
        self.layout.addWidget(self.termo_3_sensor_combo, 6, 1, 1, 2)
        self.layout.addWidget(self.watch_1_name_label, 7, 0)
        self.layout.addWidget(self.watch_1_name_input, 7, 1, 1, 2)
        self.layout.addWidget(self.watch_2_name_label, 8, 0)
        self.layout.addWidget(self.watch_2_name_input, 8, 1, 1, 2)
        self.layout.addWidget(self.watch_3_name_label, 9, 0)
        self.layout.addWidget(self.watch_3_name_input, 9, 1, 1, 2)
        self.layout.addWidget(self.ok_button, 11, 0)
        self.layout.addWidget(self.cancel_button, 11, 1, 1, 2)
        
        # Sæt layout
        self.setLayout(self.layout)
        
        # Vinduestitel
        self.setWindowTitle("Indstillinger")
        
        # Forbind knapperne med funktioner
        self.ok_button.clicked.connect(self.on_ok)
        self.cancel_button.clicked.connect(self.on_cancel)
        self.termo_1_settings_button.clicked.connect(self.open_termostat_1_settings)
        self.termo_2_settings_button.clicked.connect(self.open_termostat_2_settings)
        self.termo_3_settings_button.clicked.connect(self.open_termostat_3_settings)

    def load_settings(self):
        self.port_input.setText(self.settings.value("port", ""))
        self.termo_1_name_input.setText(self.settings.value("termo_1_name", ""))
        self.termo_1_sensor_combo.setCurrentIndex(int(self.settings.value("termo_1_sensor", 0)))
        self.termo_2_name_input.setText(self.settings.value("termo_2_name", ""))
        self.termo_2_sensor_combo.setCurrentIndex(int(self.settings.value("termo_2_sensor", 0)))
        self.termo_3_name_input.setText(self.settings.value("termo_3_name", ""))
        self.termo_3_sensor_combo.setCurrentIndex(int(self.settings.value("termo_3_sensor", 0)))
        self.watch_1_name_input.setText(self.settings.value("watch_1_name", ""))
        self.watch_2_name_input.setText(self.settings.value("watch_2_name", ""))
        self.watch_3_name_input.setText(self.settings.value("watch_3_name", ""))
        self.demo_mode_checkbox.setChecked(self.settings.value("demo_mode", False, type=bool))

    def open_termostat_1_settings(self):
        self.termostat_settings(0)

    def open_termostat_2_settings(self):
        self.termostat_settings(1)

    def open_termostat_3_settings(self):
        self.termostat_settings(2)

    def termostat_settings(self, termostat_id):
        # Åbner det nye vindue
        self.termo_settings_dialog = PIDSettingsWindow(self, termostat_id)
        self.termo_settings_dialog.show()
    
    def on_ok(self):
        self.settings.setValue("port", self.port_input.text())
        if (self.settings.value("termo_1_name", "") != self.termo_1_name_input.text()):
            self.settings.setValue("termo_1_name", self.termo_1_name_input.text())
            self.parent.parent.termostat1.set_title(self.termo_1_name_input.text())
        if (self.settings.value("termo_1_sensor", "") != self.termo_1_sensor_combo.currentIndex()):
            self.settings.setValue("termo_1_sensor", self.termo_1_sensor_combo.currentIndex())
            self.parent.parent.termostat1.set_sensor_id(self.termo_1_sensor_combo.currentIndex())
        if (self.settings.value("termo_2_name", "") != self.termo_2_name_input.text()):
            self.settings.setValue("termo_2_name", self.termo_2_name_input.text())
            self.parent.parent.termostat2.set_title(self.termo_2_name_input.text())
        if (self.settings.value("termo_2_sensor", "") != self.termo_2_sensor_combo.currentIndex()):
            self.settings.setValue("termo_2_sensor", self.termo_2_sensor_combo.currentIndex())
            self.parent.parent.termostat2.set_sensor_id(self.termo_2_sensor_combo.currentIndex())
        if (self.settings.value("termo_3_name", "") != self.termo_3_name_input.text()):
            self.settings.setValue("termo_3_name", self.termo_3_name_input.text())
            self.parent.parent.termostat3.set_title(self.termo_3_name_input.text())
        if (self.settings.value("termo_3_sensor", "") != self.termo_3_sensor_combo.currentIndex()):
            self.settings.setValue("termo_3_sensor", self.termo_3_sensor_combo.currentIndex())
            self.parent.parent.termostat3.set_sensor_id(self.termo_3_sensor_combo.currentIndex())
        if (self.settings.value("watch_1_name", "") != self.watch_1_name_input.text()):
            self.settings.setValue("watch_1_name", self.watch_1_name_input.text())
            self.parent.parent.watch.set_name(0, self.watch_1_name_input.text())
        if (self.settings.value("watch_2_name", "") != self.watch_2_name_input.text()):
            self.settings.setValue("watch_2_name", self.watch_2_name_input.text())
            self.parent.parent.watch.set_name(1, self.watch_2_name_input.text())
        if (self.settings.value("watch_3_name", "") != self.watch_1_name_input.text()):
            self.settings.setValue("watch_3_name", self.watch_3_name_input.text())
            self.parent.parent.watch.set_name(2, self.watch_3_name_input.text())
        self.settings.setValue("demo_mode", self.demo_mode_checkbox.isChecked())

        self.close()  # Luk vinduet efter OK

    def on_cancel(self):
        # Håndter Cancel knap klik
        self.close()  # Luk vinduet efter Cancel
