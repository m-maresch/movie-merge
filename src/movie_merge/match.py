import os

import cv2
import numpy as np
from tqdm import tqdm

from filter import is_interesting
from format import format_time


def find_best_match(video1_path, video2_path, start_v1=0, end_v2=None, stride=10):
    cap1 = cv2.VideoCapture(video1_path)
    cap2 = cv2.VideoCapture(video2_path)

    frames1 = int(cap1.get(cv2.CAP_PROP_FRAME_COUNT))

    hashes1 = []
    indices1 = []

    fps1 = cap1.get(cv2.CAP_PROP_FPS)
    fps2 = cap2.get(cv2.CAP_PROP_FPS)

    # Convert time arguments (seconds) to frame indices
    start_frame_v1 = int(start_v1 * fps1)
    total_frames_v2 = int(cap2.get(cv2.CAP_PROP_FRAME_COUNT))
    end_frame_v2 = int(end_v2 * fps2) if end_v2 else total_frames_v2

    print(
        f"--- Indexing {os.path.basename(video1_path)} (from {format_time(start_v1)}, every {stride}th frame) ---"
    )
    cap1.set(cv2.CAP_PROP_POS_FRAMES, start_frame_v1)
    for i in tqdm(range(start_frame_v1, frames1, stride)):
        ret, frame = cap1.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if is_interesting(gray):
            hashes1.append(cv2.resize(gray, (64, 64)))
            indices1.append(i)
        # Skip frames to maintain stride
        for _ in range(stride - 1):
            cap1.grab()

    if not hashes1:
        print(
            "Error: No 'interesting' frames found in video 1. Is the video e.g. all black?"
        )
        return (0, 0)

    stack1 = np.array(hashes1, dtype=np.int16)
    best_diff = float("inf")
    best_pair = (0, 0)

    print(
        f"--- Scanning {os.path.basename(video2_path)} (until {format_time(end_v2)}) ---"
    )
    for i2 in tqdm(range(0, end_frame_v2, stride)):
        ret, frame2 = cap2.read()
        if not ret:
            break
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        if not is_interesting(gray2):
            continue

        h2 = cv2.resize(gray2, (64, 64)).astype(np.int16)
        diffs = np.sum(np.abs(stack1 - h2), axis=(1, 2))
        min_idx = np.argmin(diffs)

        if diffs[min_idx] < best_diff:
            best_diff, best_pair = diffs[min_idx], (indices1[min_idx], i2)
        for _ in range(stride - 1):
            cap2.grab()

    cap1.release()
    cap2.release()

    return best_pair
