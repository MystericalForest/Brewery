import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout,
    QWidget, QPushButton, QLineEdit, QSizePolicy
)
from PyQt5.QtCore import QTimer, Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd

class TemperaturePlot(FigureCanvas):
#    def __init__(self, name, log_data, parent=None):
        df = pd.DataFrame(log_data)
        df.set_index("timestamp", inplace=True)
        
    def __init__(self, name, temperature_data, time_data, setpoint_data, heater_data, parent=None):
        self.fig, self.ax = plt.subplots()
        super().__init__(self.fig)
        self.setParent(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # <- Denne linje!
        self.name = name

        self.temperature_data = temperature_data
        self.time_data = time_data
        self.setpoint_data = setpoint_data
        self.heater_data = heater_data
        self.max_points = 100

        self.ax.set_title(self.name)
        self.ax.set_ylabel("Temperatur (°C)")
        self.ax.set_xlabel("Tid (s)")
        self.ax2 = self.ax.twinx()  # Sekundær Y-akse til heater

    def update_plot(self, current_temp, setpoint, heater_on, elapsed_time):
        self.temperature_data.append(current_temp)
        changed_data=True if ((self.setpoint_data[-1] != setpoint) or (self.heater_data[-1] != heater_on)) else False
        if (changed_data):
            self.time_data.append(elapsed_time)
            self.temperature_data.append(current_temp)
            self.setpoint_data.append(self.setpoint_data[-1])
            self.heater_data.append(self.heater_data[-1])
        self.setpoint_data.append(setpoint)
        self.heater_data.append(1 if heater_on else 0)
        self.time_data.append(elapsed_time)

        # Trim dataserier
        if len(self.time_data) > self.max_points:
            self.temperature_data = self.temperature_data[-self.max_points:]
            self.setpoint_data = self.setpoint_data[-self.max_points:]
            self.heater_data = self.heater_data[-self.max_points:]
            self.time_data = self.time_data[-self.max_points:]

        self.ax.clear()
        self.ax2.clear()

        self.ax.plot(self.time_data, self.temperature_data, label="Temperatur", color='blue')
        self.ax.plot(self.time_data, self.setpoint_data, label="Setpoint", color='red', linestyle='--')
        self.ax.set_ylim(10, max(max(self.temperature_data + self.setpoint_data), 30) + 15)
        self.ax.set_xlabel("Tid (s)")
        self.ax.set_ylabel("Temperatur (°C)")

        # Sekundær akse for varmelegeme
        self.ax2.plot(self.time_data, self.heater_data, label="Varmelegeme", color='grey', linestyle=':', linewidth=2)
        #self.ax2.set_ylabel("")
        self.ax2.set_ylim(-0.1, 1.3)

        self.ax.set_title(self.name)
        self.ax.legend(loc="upper left")
        self.ax2.legend(loc="upper right")

        self.draw()

class TermostatGraf(QMainWindow):
    def __init__(self, name, log_data=None, parent=None):
        super().__init__()
        if (log_data is None):
            self.name = name + ": Demodata"
        else:
            self.name = name
        self.setWindowTitle(self.name)
        self.log_data = log_data
        self.parent = parent

        # Setpoint og tilstand
        self.setpoint = 50.0
        self.elapsed_time = 0
        self.current_temp = 35.0
        self.heater_on = False

        # Layout
        main_layout = QVBoxLayout()

        # Hovedindhold (labels + graf)
        content_layout = QHBoxLayout()

        # Højre kolonne
        self.temp_label = QLabel("0.0 °C")
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.temp_label.setStyleSheet("font-size: 36px; font-weight: bold; margin: 10px;")
        self.setpoint_label = QLabel("(0.0 °C)")
        self.setpoint_label.setAlignment(Qt.AlignCenter)
        self.setpoint_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 10px;")
        self.heater_label = QLabel("Varmelegeme: FRA")
        self.heater_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        self.setpoint_input = QLineEdit(str(self.setpoint))
        self.setpoint_input.returnPressed.connect(self.update_setpoint) 
        self.update_button = QPushButton("Opdater Setpoint")
        self.update_button.clicked.connect(self.update_setpoint)

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.temp_label)
        left_layout.addWidget(self.setpoint_label)
        left_layout.addWidget(self.heater_label)
        left_layout.addWidget(self.setpoint_input)
        left_layout.addWidget(self.update_button)
        left_layout.addStretch()

        # Venstre kolonne: graf
        self.elapsed_time=5
        temperature_data = [23,22,22,21,21,22,21,21]
        time_data = [1,2,2,3,3,4,5,5]
        setpoint_data = [21,21,21,21,25,25,25,50]
        heater_data = [True, True, False, False, False, False, False, True]
        self.plot = TemperaturePlot(self.name, temperature_data, time_data, setpoint_data, heater_data, self)
#        self.plot = TemperaturePlot(self.name, self.log_data, self)

        # Saml layout
        content_layout.addWidget(self.plot, stretch=3)
        content_layout.addLayout(left_layout, stretch=1)
        main_layout.addLayout(content_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Timer til opdatering
        self.timer = QTimer()
        self.timer.setInterval(1000)  # 1 sekund
        self.timer.timeout.connect(self.update_data)
        self.timer.start()

    def update_setpoint(self):
        try:
            self.setpoint = float(self.setpoint_input.text())
            self.parent.update_setpoint(self.setpoint)
        except ValueError:
            pass  # Ignorer ugyldigt input

    def update_data(self):
        self.elapsed_time += 1

        # Simuleret temperatur (udskift med rigtig måling hvis nødvendigt)
        self.current_temp += random.uniform(-0.5, 0.5)

        # Simpel styring
        self.heater_on = self.current_temp < self.setpoint

        # Opdater labels
        self.temp_label.setText(f"{self.current_temp:.1f} °C")
        self.setpoint_label.setText(f"({self.setpoint:.1f}) °C")
        self.heater_label.setText(f"Varmelegeme: {'TIL' if self.heater_on else 'FRA'}")

        # Opdater graf
        self.plot.update_plot(
            self.current_temp,
            self.setpoint,
            self.heater_on,
            self.elapsed_time
        )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TermostatGraf("Gryde 1")
    window.show()
    sys.exit(app.exec_())
