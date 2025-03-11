from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QLineEdit, QSlider, QDialog, QGroupBox
import datetime

class Watch:
    def __init__(self, seconds):
        self.seconds = seconds
        self.remainer_seconds = seconds
        self.running = False
        
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

class WatchWidget(QWidget):
    def __init__(self, watch1_name, watch2_name, watch3_name):
        super().__init__()
        
        self.clWatch = Watch(1000)
        
        self.watch1 = QLabel(self.clWatch.get_time_as_text(), self)
        self.watch1.setAlignment(Qt.AlignCenter)
        self.watch1.setStyleSheet("font-size: 40px;")
        
        self.watch_label1 = QLabel(watch1_name, self)
        self.watch_label1.setAlignment(Qt.AlignCenter)
        self.watch_label1.setStyleSheet("font-size: 18px;")
        
        self.watch2 = QLabel("22:53", self)
        self.watch2.setAlignment(Qt.AlignCenter)
        self.watch2.setStyleSheet("font-size: 40px;")
        
        self.watch_label2 = QLabel(watch2_name, self)
        self.watch_label2.setAlignment(Qt.AlignCenter)
        self.watch_label2.setStyleSheet("font-size: 18px;")
        
        self.watch3 = QLabel("08:26", self)
        self.watch3.setAlignment(Qt.AlignCenter)
        self.watch3.setStyleSheet("font-size: 40px;")
        
        self.watch_label3 = QLabel(watch3_name, self)
        self.watch_label3.setAlignment(Qt.AlignCenter)
        self.watch_label3.setStyleSheet("font-size: 18px;")

        # Opret layout
        layout = QGridLayout()
        layout.addWidget(self.watch1, 0, 0)
        layout.addWidget(self.watch2, 0, 1)
        layout.addWidget(self.watch3, 0, 2)
        layout.addWidget(self.watch_label1, 1, 0)
        layout.addWidget(self.watch_label2, 1, 1)
        layout.addWidget(self.watch_label3, 1, 2)

        self.setLayout(layout)

    def get_widget(self):
        return self
