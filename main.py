import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from pyqtgraph.dockarea import DockArea
from pyqtgraph.dockarea.Dock import Dock
import pyqtgraph as pg

from screens.main_screen import MainScreen
from screens.parameters import Parameters

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_main_screen()
        self.init_parameter_screen()
        self.setCentralWidget(self.area)

    def init_ui(self):
        self.setWindowTitle("Mouse Tracker")
        self.setGeometry(100, 100, 800, 600)

        self.area = DockArea()
        
        self.parameters_dock = Dock("Parameters", size=(0.25, 1), hideTitle=True, closable=False) # Area for displaying the parameters (left side of the window)
        self.main_screen_dock = Dock("Main Screen", size=(0.75, 1), hideTitle=True, closable=False) # Area for displaying the main screen

        self.area.addDock(self.parameters_dock, "left")
        self.area.addDock(self.main_screen_dock, "right")

    def init_parameter_screen(self):
        self.param_screen = Parameters()
        self.param_screen.analyzeCompleted.connect(self.main_screen.upload_data)
        self.parameters_dock.addWidget(self.param_screen)

    def init_main_screen(self):
        self.main_screen = MainScreen()
        self.main_screen_dock.addWidget(self.main_screen)
    

        

if __name__ == "__main__": 
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())