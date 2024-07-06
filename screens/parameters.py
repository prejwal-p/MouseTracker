from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QHBoxLayout, QPushButton, QMessageBox, QSpinBox, QCheckBox
from PyQt5.QtWidgets import QFileDialog
from pyqtspinner import WaitingSpinner
import time
import threading
from PyQt5.QtCore import pyqtSignal
import numpy as np

from functions.functions import Functions

class Parameters(QWidget):
    analyzeCompleted = pyqtSignal(str, dict, dict, int, int)

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.file_name = None
        self.setLayout(self.param_layout)

    def init_ui(self):
        self.param_layout = QVBoxLayout()

        # File Selector Box
        self.file_selector_box = QGroupBox("Select File")
        self.file_selector_layout = QHBoxLayout()

        select_file_label = QLabel("Select the Video File:")
        self.file_selector_layout.addWidget(select_file_label)
        self.select_file_button = QPushButton("Browse")
        self.select_file_button.clicked.connect(self.select_file)
        self.file_selector_layout.addWidget(self.select_file_button)

        self.file_selector_box.setLayout(self.file_selector_layout)

        self.param_layout.addWidget(self.file_selector_box)

        # Adding a test button checck and spinbox for the number of frames
        self.test_button = QCheckBox("Test Mode (Display Only Few Frames)")
        self.param_layout.addWidget(self.test_button)
        self.test_button.stateChanged.connect(self.test_mode)

        self.frame_spinbox = QSpinBox()
        self.frame_spinbox.setMinimum(0)
        self.frame_spinbox.setMaximum(1000)
        self.frame_spinbox.setValue(250)
        self.frame_spinbox.setEnabled(False)


        self.param_layout.addWidget(self.frame_spinbox)


        # Analyze Button
        self.analyze_button = QPushButton("Analyze")
        self.analyze_button.clicked.connect(self.analyze)
        self.param_layout.addWidget(self.analyze_button)

    def test_mode(self):
        if self.test_button.isChecked():
            self.frame_spinbox.setEnabled(True)
        else:
            self.frame_spinbox.setEnabled(False)

    def select_file(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Video Files (*.mp4 *.avi)")
        file_dialog.setViewMode(QFileDialog.Detail)
        file_dialog.setDirectory(".")

        if file_dialog.exec_():
            file_name = file_dialog.selectedFiles()
            self.file_name = file_name[0]

    def analyze(self):
        if self.file_name is None:
            QMessageBox.warning(self, "Error", "Please select a file first.")
            return
        
        # Start the spinner
        self.spinner = WaitingSpinner(self, True, True)
        self.spinner.start()
        self.thread = threading.Thread(target=self.analyze_video, args=(self.spinner,))
        self.thread.start()
        
        print("Analyzing the video...")
        # Call the analyze function
        
    def analyze_video(self, spinner):
        functions = Functions()
        background = functions.get_background(self.file_name)
        print("Background obtained")

        if self.test_button.isChecked():
            total_frames = self.frame_spinbox.value()
        else:
            total_frames = None

        centroid, countour_array, frame_rate, total_frames = functions.get_countours(self.file_name, background, total_frames)
        print("Contours obtained")
        
        self.analyzeCompleted.emit(self.file_name, centroid, countour_array, frame_rate, total_frames)
        spinner.stop()
        


        