"""
@author: Javier Perez
@email: javier_e_perez21@hotmail.com
"""

import cv2
import numpy as np

# Global Variables
HMIN = 0
HMAX = 180
SMIN = 0
SMAX = 255
VMIN = 0
VMAX = 255

def callback_hue_min(value):
    global HMIN
    HMIN = value


def callback_hue_max(value):
    global HMAX
    HMAX = value


def callback_saturation_min(value):
    global SMIN
    SMIN = value


def callback_saturation_max(value):
    global SMAX
    SMAX = value


def callback_value_min(value):
    global VMIN
    VMIN = value


def callback_value_max(value):
    global VMAX
    VMAX = value


def apply_color_filter(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    H = hsv[:, :, 0]
    S = hsv[:, :, 1]
    V = hsv[:, :, 2]

    # define range of blue color in HSV
    lower = np.array([HMIN, SMIN, VMIN])
    upper = np.array([HMAX, SMAX, VMAX])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower, upper)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(img, img, mask=mask)

    return res


# ---Constants, Tunable params---
# subsample ratio is used to downsize the camera image.
subsamplingRatio = 0.5
windowName = 'TrackBars'
cv2.namedWindow(windowName)

# --TRACK-BARS--
# HUE
cv2.createTrackbar('Hmin',     # Track-bar name
                   windowName,  # Window to Draw track-bar
                   0,         # Track-bar default position
                   180,         # Track-bar Max positiong
                   callback_hue_min)    # track-bar callback
cv2.createTrackbar('Hmax',     # Track-bar name
                   windowName,  # Window to Draw track-bar
                   180,         # Track-bar default position
                   180,         # Track-bar Max positiong
                   callback_hue_max)    # track-bar callback
# SATURATION
cv2.createTrackbar('Smin',     # Track-bar name
                   windowName,  # Window to Draw track-bar
                   0,         # Track-bar default position
                   255,         # Track-bar Max positiong
                   callback_saturation_min)    # track-bar callback
cv2.createTrackbar('Smax',     # Track-bar name
                   windowName,  # Window to Draw track-bar
                   255,         # Track-bar default position
                   255,         # Track-bar Max positiong
                   callback_saturation_max)    # track-bar callback
# VALUE
cv2.createTrackbar('Vmin',     # Track-bar name
                   windowName,  # Window to Draw track-bar
                   0,         # Track-bar default position
                   255,         # Track-bar Max positiong
                   callback_value_min)    # track-bar callback
cv2.createTrackbar('Vmax',     # Track-bar name
                   windowName,  # Window to Draw track-bar
                   255,         # Track-bar default position
                   255,         # Track-bar Max positiong
                   callback_value_max)    # track-bar callback

cap = cv2.VideoCapture(0)
print('Cancel the camera capture by pressing \'q\'')
while True:
    # Capture frame-by-frame
    ret, cameraFrameColor = cap.read()
    if ret is not True:
        break

    # Pre-process the Camera frame, resize and get HSV image
    cameraFrameColor = cv2.resize(cameraFrameColor, (0, 0), fx=subsamplingRatio, fy=subsamplingRatio)

    # Process the image
    result = apply_color_filter(cameraFrameColor)

    # Display the resulting frame
    cv2.imshow('Result', result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
