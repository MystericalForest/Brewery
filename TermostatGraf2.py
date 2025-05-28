import sys
import random
import matplotlib
matplotlib.use("QtAgg")

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout,
    QWidget, QPushButton, QLineEdit, QSizePolicy
)
from PyQt5.QtCore import QTimer, Qt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd

class TemperaturePlot(FigureCanvas):
    def __init__(self, name, logger, parent=None):
        
        self.fig, self.ax = plt.subplots()
        super().__init__(self.fig)
        self.setParent(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # <- Denne linje!
        self.name = name

        self.ax.set_title(self.name)
        self.ax.set_ylabel("Temperatur (°C)", color="black")
        self.ax.set_xlabel("Tid (s)")
        self.ax2 = self.ax.twinx()  # Sekundær Y-akse til heater
        self.ax2.set_ylabel("Heating", color="green")
        
 #       self.update_plot(logger.get_log())

    def update_plot(self, data):
        self.ax.clear()
        self.ax2.clear()
        
        self.ax.plot(data['timestamp'], data['setpoint'], 'b--', label='Setpoint')
        self.ax.plot(data['timestamp'], data['temperatur'], 'r--', label='Temperatur')
        self.ax2.plot(data['timestamp'], data['heating'], 'g--', label='Heating')
        
        self.ax.set_ylim(0, 110)
        self.ax2.set_ylim(-0.1, 1.3)

        self.ax.set_xlabel("Tid (s)")
        self.ax.set_ylabel("Temperatur (°C)")

        self.ax.legend(loc="upper left")
        self.ax2.legend(loc="upper right")
        
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        self.fig.autofmt_xdate()

        self.draw()

class TermostatGraf(QMainWindow):
    def __init__(self, name, logger=None, parent=None):
        super().__init__()
        if (logger is None):
            self.name = name + ": No data"
        else:
            self.name = name
        self.setWindowTitle(self.name)
        self.logger = logger
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
        self.save_button = QPushButton("Gem data som csv")
        self.save_button.clicked.connect(self.save_data)

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.temp_label)
        left_layout.addWidget(self.setpoint_label)
        left_layout.addWidget(self.heater_label)
        left_layout.addWidget(self.setpoint_input)
        left_layout.addWidget(self.update_button)
        left_layout.addWidget(self.save_button)
        left_layout.addStretch()

        self.plot = TemperaturePlot(self.name, self.logger, self)

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
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_setpoint(self):
        try:
            self.setpoint = float(self.setpoint_input.text())
            self.parent.update_setpoint(self.setpoint)
        except ValueError:
            pass  # Ignorer ugyldigt input

    def save_data(self):
        self.logger.save_to_file("Termostat_" + self.parent.title)
        
    def update_plot(self):
        log = self.logger.get_log()
        last_entry = self.logger.get_last_entry()
        if not log:
            return
        self.temp_label.setText(f"{self.parent.temperature:.1f} °C")
        self.setpoint_label.setText(f"({self.parent.setpoint:.1f})")
        if (self.parent.heating):
            self.heater_label.setText("Varmelegeme: TIL")
        else:
            self.heater_label.setText("Varmelegeme: FRA")
        df = pd.DataFrame(log)
        df = df.sort_values('timestamp')
        self.plot.update_plot(df)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TermostatGraf("Gryde 1")
    window.show()
    sys.exit(app.exec_())
