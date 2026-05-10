import numpy as np


def is_interesting(frame_gray, brightness_threshold=15, std_threshold=5):
    """
    Determines if a frame is 'interesting' (is real content vs e.g. just a black screen).
    """
    mean = np.mean(frame_gray)
    std = np.std(frame_gray)
    return mean > brightness_threshold and std > std_threshold
