from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QLineEdit, QSlider, QDialog, QGroupBox, QSpinBox
import datetime

class TimerDialog(QDialog):
    def __init__(self, name, seconds):
        super().__init__()

        # Opsætning af det nye vindue
        self.setWindowTitle("Ret tider")
        self.setGeometry(200, 200, 300, 200)

        self.name = name

        self.hours = seconds // 3600  # 1 time = 3600 sekunder
        seconds = seconds % 3600  # Resten af sekunderne efter timerne
        self.minutes = seconds // 60  # 1 minut = 60 sekunder
        self.seconds = seconds % 60  # Resten af sekunderne efter minutterne
        
        # Layout og inputfelter
        layout = QGridLayout()
        
        # Slider
        self.label = QLabel(self.name, self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 24px;")
        
        self.hour_label = QLabel("Timer:", self)
        self.hour_label.setAlignment(Qt.AlignLeft)
        self.hour_label.setStyleSheet("font-size: 12px;")
        self.hour_slider = QSlider(Qt.Horizontal, self)
        self.hour_slider.setRange(0, 10)  # Sætter intervallet for slideren
        self.hour_slider.setTickPosition(QSlider.TicksBelow)
        self.hour_slider.setTickInterval(1)
        self.hour_slider.setValue(self.hours) 
        self.hour_slider.valueChanged.connect(self.update_value)
        
        self.minute_label = QLabel("Minutter:", self)
        self.minute_label.setAlignment(Qt.AlignLeft)
        self.minute_label.setStyleSheet("font-size: 12px;")
        self.minute_slider = QSlider(Qt.Horizontal, self)
        self.minute_slider.setRange(0, 59)  # Sætter intervallet for slideren
        self.minute_slider.setTickPosition(QSlider.TicksBelow)
        self.minute_slider.setTickInterval(10)
        self.minute_slider.setValue(self.minutes) 
        self.minute_slider.valueChanged.connect(self.update_value)
        
        self.second_label = QLabel("Sekunder:", self)
        self.second_label.setAlignment(Qt.AlignLeft)
        self.second_label.setStyleSheet("font-size: 12px;")
        self.second_slider = QSlider(Qt.Horizontal, self)
        self.second_slider.setRange(0, 59)  # Sætter intervallet for slideren
        self.second_slider.setTickPosition(QSlider.TicksBelow)
        self.second_slider.setTickInterval(10)
        self.second_slider.setValue(self.seconds) 
        self.second_slider.valueChanged.connect(self.update_value)
        
        self.value = QLabel(f"{self.hours}:{self.minutes:02}:{self.seconds:02}", self)
        self.value.setAlignment(Qt.AlignCenter)
        self.value.setStyleSheet("font-size: 48px;")
        layout.addWidget(self.label,0,0, 1, 2)
        layout.addWidget(self.value,1,0, 1, 2)
        layout.addWidget(self.hour_label,2,0, 1, 2)
        layout.addWidget(self.hour_slider,3,0, 1, 2)
        layout.addWidget(self.minute_label,4,0, 1, 2)
        layout.addWidget(self.minute_slider,5,0, 1, 2)
        layout.addWidget(self.second_label,6,0, 1, 2)
        layout.addWidget(self.second_slider,7,0, 1, 2)

        self.ok_button = QPushButton('Ok', self)
        self.ok_button.clicked.connect(self.ok_clicked)
        layout.addWidget(self.ok_button,8,0)
 
        self.cancel_button = QPushButton('Cancel', self)
        self.cancel_button.clicked.connect(self.cancel_clicked)
        layout.addWidget(self.cancel_button,8,1)

        self.setLayout(layout)
    
    def update_value(self):
        self.hours = self.hour_slider.value()
        self.minutes = self.minute_slider.value()
        self.seconds = self.second_slider.value()
        self.total_seconds = self.hours * 3600 + self.minutes * 60 + self.seconds
        self.value.setText(f"{self.hours}:{self.minutes:02}:{self.seconds:02}")
        
    def ok_clicked(self):
        self.accept()  # Lukker dialogen efter overførsel

    def cancel_clicked(self):
        self.reject()
        
class Watch(QWidget):
    def __init__(self, name, seconds):
        super().__init__()
        self.seconds = seconds
        self.remainer_seconds = seconds
        self.name = name
        self.running = False
        self.reset_mode=True
        
        self.watch = QLabel(self.get_time_as_text(), self)
        self.watch.setAlignment(Qt.AlignCenter)
        self.watch.setStyleSheet("font-size: 40px;")
        
        self.watch_label = QLabel(name, self)
        self.watch_label.setAlignment(Qt.AlignCenter)
        self.watch_label.setStyleSheet("font-size: 18px;")

        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.start) 
        self.start_button.setEnabled(True)
 
        self.stop_button = QPushButton('Reset time', self)
        self.stop_button.clicked.connect(self.stop)
        self.stop_button.setEnabled(True)

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

    def set_name(self, name):
        self.name = name
        self.watch_label.setText(self.name)
        
    def start(self):
        self.running = True
        self.reset_mode = False
        self.stop_button.setText("Stop")
        self.start_button.setEnabled(False)
        
    def stop(self):
        self.running = False
        if (self.reset_mode):
            self.remainer_seconds = self.seconds
            self.TimerDialog = TimerDialog(self.name, self.seconds)
            if self.TimerDialog.exec_()  == QDialog.Accepted:
                self.seconds = self.TimerDialog.total_seconds
                self.remainer_seconds = self.TimerDialog.total_seconds
            
        self.stop_button.setText("Reset time")
        self.reset_mode=True
        self.start_button.setEnabled(True)
        
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

    def set_name(self, watch_id, name):
        if (watch_id==0):
            self.watch1.set_name(name)
        if (watch_id==1):
            self.watch2.set_name(name)
        if (watch_id==2):
            self.watch3.set_name(name)

    def set_time(self, second1, second2, second3):
        self.watch1.set_time(second1)
        self.watch2.set_time(second2)
        self.watch3.set_time(second3)
