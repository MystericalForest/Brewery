from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QLineEdit, QSlider, QDialog, QGroupBox
import datetime

class Watch(QWidget):
    def __init__(self, name, seconds):
        super().__init__()
        self.seconds = seconds
        self.remainer_seconds = seconds
        self.running = False
        
        self.watch = QLabel(self.get_time_as_text(), self)
        self.watch.setAlignment(Qt.AlignCenter)
        self.watch.setStyleSheet("font-size: 40px;")
        
        self.watch_label = QLabel(name, self)
        self.watch_label.setAlignment(Qt.AlignCenter)
        self.watch_label.setStyleSheet("font-size: 18px;")

        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.start) 
        self.start_button.enabled = True
 
        self.stop_button = QPushButton('Stop', self)
        self.stop_button.clicked.connect(self.stop)
        self.stop_button.enabled = False

        # Opret layout
        layout = QGridLayout()
        layout.addWidget(self.watch, 0, 0, 1, 2)
        layout.addWidget(self.watch_label, 1, 0, 1, 2)
        layout.addWidget(self.start_button, 2, 0)
        layout.addWidget(self.stop_button, 2, 1)

        self.setLayout(layout)

        timer = QTimer(self, interval=1000, timeout=self.handle_timeout)
        timer.start()

    def paintEvent(self, event):
        self.watch.setText(self.get_time_as_text())

    def handle_timeout(self):
        if (self.running): 
            self.remainer_seconds = self.remainer_seconds - 1
            self.update()

    def get_widget(self):
        return self
        
    def start(self):
        self.running = True
        
    def stop(self):
        self.running = False
        
    def reset(self):
        self.running = False
        self.remainer_seconds = self.seconds
        
    def get_time_as_text(self):
        return str(datetime.timedelta(seconds=self.remainer_seconds))
        
    def set_time(self, seconds):
        self.seconds = seconds
        self.remainer_seconds = seconds
        self.update()

class WatchWidget(QWidget):
    def __init__(self, watch1_name, watch2_name, watch3_name):
        super().__init__()
        
        self.watch1 = Watch(watch1_name, 1000)
        self.watch2 = Watch(watch2_name, 1000)
        self.watch3 = Watch(watch3_name, 1000)
        
        # Opret layout
        layout = QGridLayout()
        layout.addWidget(self.watch1, 0, 0)
        layout.addWidget(self.watch2, 0, 1)
        layout.addWidget(self.watch3, 0, 2)

        self.setLayout(layout)

    def get_widget(self):
        return self

    def set_time(self, second1, second2, second3):
        self.watch1.set_time(second1)
        self.watch2.set_time(second2)
        self.watch3.set_time(second3)
