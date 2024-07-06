import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cv2
import time
from scipy.signal import medfilt


class Functions:
    def __init__(self):
        pass

    def get_background(self, video_path):
        video = cv2.VideoCapture(video_path)

        # Temporal Median Filtering
        image_shape = (int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(video.get(cv2.CAP_PROP_FRAME_WIDTH)))
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

        frame_array = []

        # Getting index a total 200 images from the video
        if total_frames < 200:
            index = np.arange(0, total_frames, 1)
        else:
            index = np.arange(0, total_frames, total_frames//200)
        
        for i in index:
            video.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = video.read()
            if not ret:
                break
            frame_array.append(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))

        frame_array = np.array(np.transpose(frame_array, axes=(1, 2, 0)))
        median_frame = np.median(np.array(frame_array), axis=2).astype(np.uint8)

        video.release()

        return median_frame

    def get_countours(self, video_path, median_frame, total_frames=None):
        video = cv2.VideoCapture(video_path)
        frame_rate = int(video.get(cv2.CAP_PROP_FPS))
        centroid = {}
        i = 0

        countour_array = {}

        if total_frames is None:
            total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))


        for i in range(total_frames):
            ret, frame = video.read()
            if not ret:
                break
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            subtracted = cv2.absdiff(frame, median_frame)

            kernelSize = (25,25)
            frameBlur = cv2.GaussianBlur(subtracted, kernelSize, 0)
            _, thresh = cv2.threshold(frameBlur, 50, 255, cv2.THRESH_BINARY)

            countours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            # Getting the largest contour
            if len(countours) > 0:
                max_contour = max(countours, key=cv2.contourArea)
                # Calculating centroid of the mouse
                M = cv2.moments(max_contour)
                if M['m00'] != 0:
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])

                centroid[i] = (cx, cy)
                countour_array[i] = countours

            i += 1

        # Filtering centroid
        filter_size = int(0.5 * frame_rate)

        if filter_size % 2 == 0:
            filter_size += 1

        x_values = [x for x, y in centroid.values()]
        y_values = [y for x, y in centroid.values()]
        x_values = medfilt(x_values, kernel_size=filter_size)
        y_values = medfilt(y_values, kernel_size=filter_size)

        centroid = {i: (x_values[i], y_values[i]) for i in range(len(x_values))}
        
        video.release()
            
        return centroid, countour_array, frame_rate, total_frames


