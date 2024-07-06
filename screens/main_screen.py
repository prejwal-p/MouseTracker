from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QHBoxLayout, QPushButton, QMessageBox, QSlider, QPushButton
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
import cv2

class MainScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.play_state = False
        self.current_frame = 0

    def init_ui(self):
        self.param_layout = QVBoxLayout()

        self.video_area = pg.GraphicsLayoutWidget()
        self.view = self.video_area.addViewBox()
        self.view.setAspectLocked(True)

        self.img = pg.ImageItem()
        self.view.addItem(self.img)
        
        self.param_layout.addWidget(self.video_area)
        self.setLayout(self.param_layout)

        # Adding a slide and play pause button
        self.play_pause_button = QPushButton("Play")
        self.play_pause_button.clicked.connect(self.play_pause)
        self.param_layout.addWidget(self.play_pause_button)

        self.slider = QSlider(QtCore.Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(0)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(1)
        self.slider.valueChanged.connect(self.scroll_video)
        self.param_layout.addWidget(self.slider)


    def timer_logic(self):
        self.updateTimer = QtCore.QTimer()
        self.updateTimer.timeout.connect(self.update)
        self.updateTimer.start(int(1000/self.frame_rate))

    def update(self):
        if self.play_state:
            self.current_frame += 1
            if self.current_frame >= self.total_frames:
                self.current_frame = 0

            return_value, frame = self.video.read()
            if not return_value:
                self.updateTimer.stop()
                return
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = self.draw_contours(frame)



            self.img.setImage(frame)
            self.slider.setValue(self.current_frame)
            
            QtCore.QCoreApplication.processEvents()
        else:
            self.updateTimer.stop()

    def play_pause(self):
        if self.play_state:
            self.play_state = False
            self.play_pause_button.setText("Play")
        else:
            self.play_state = True
            self.play_pause_button.setText("Pause")
            self.timer_logic()

    def scroll_video(self):
        self.current_frame = self.slider.value()
        self.video.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
    

    def upload_data(self, filename, centroid, countour_array, frame_rate, total_frames):
        self.video = cv2.VideoCapture(filename)
        self.frame_rate = frame_rate
        self.centroid = centroid
        self.countour_array = countour_array
        self.data = []
        self.total_frames = total_frames
        self.slider.setMaximum(self.total_frames)
        self.slider.setValue(0)

        print(len(self.centroid.values()), len(self.countour_array.values()), self.total_frames) 


    def draw_contours(self, img):
        try:
            centroid = self.centroid[self.current_frame]
            countours = self.countour_array[self.current_frame]

            for contour in countours:
                hull = cv2.convexHull(contour, returnPoints=False)
                defects = cv2.convexityDefects(contour, hull)

                cv2.drawContours(img, [contour], -1, (0, 255, 0), 2)

            # Drawing centroid
            cv2.circle(img, centroid, 5, (0, 0, 255), -1)
        except:
            return img

        return img


