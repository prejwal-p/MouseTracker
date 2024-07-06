# Mouse Tracker
## Current Version: v0.1

Software to help you track animal trajectories for behavioral experiments.

### Pipeline
1. Use temporal median filtering to obtain the background images.
2. The background image is subtracted from all frames.
3. Thresholding and contour detection are performed to get the contour and center point of the animal. 
4. The obtained centroids are filtered to remove outliers.

### Installation
1. Clone this repository.
2. Run: `conda create --name {you_env_name} --file requirements.yml`

### Single Animal Tracking
This works best for a single animal.
![mouse](https://github.com/prejwal-p/MouseTracker/blob/main/images/mouse.gif)

### Multi Animal Tracking
The centroid detection in multi-animals does not work very well.
![fly](https://github.com/prejwal-p/MouseTracker/blob/main/images/fly.gif)


### Upcoming Features:
1. Improved multi-animal centroid detection.
2. Select an object in frame (using SegmentAnything)
3. Calculate distance from objects. 
