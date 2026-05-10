import argparse
import os

import cv2

from format import format_time
from display import show_common_frame
from match import find_best_match
from movie import trim_and_merge


def main():
    parser = argparse.ArgumentParser(
        description="Merge two videos by finding a common frame."
    )
    parser.add_argument("file1", help="Path to the first video file (the start)")
    parser.add_argument("file2", help="Path to the second video file (the end)")
    parser.add_argument(
        "-n",
        "--every-nth-frame",
        type=int,
        default=1,
        dest="stride",
        help="Sample rate for video scanning. E.g. 1 = every frame (default), 10 = every 10th frame.",
    )
    parser.add_argument(
        "--start-at-min",
        type=float,
        default=0.0,
        help="Minutes into File 1 to start searching.",
    )
    parser.add_argument(
        "--end-at-min",
        type=float,
        default=None,
        help="Minutes into File 2 to stop searching.",
    )

    args = parser.parse_args()
    path1 = args.file1
    path2 = args.file2
    start_at_sec = args.start_at_min * 60
    end_at_sec = args.end_at_min * 60 if args.end_at_min is not None else None
    stride = args.stride

    v1_temp = cv2.VideoCapture(path1)
    v2_temp = cv2.VideoCapture(path2)
    fps1 = v1_temp.get(cv2.CAP_PROP_FPS)
    fps2 = v2_temp.get(cv2.CAP_PROP_FPS)
    v1_temp.release()
    v2_temp.release()

    # 1. Determine common frame
    idx1, idx2 = find_best_match(path1, path2, start_at_sec, end_at_sec, stride)
    time1 = idx1 / fps1
    time2 = idx2 / fps2

    print("\n--- MATCH IDENTIFIED ---")
    print(f"File 1: {os.path.basename(path1)} at **{format_time(time1)}**")
    print(f"File 2: {os.path.basename(path2)} at **{format_time(time2)}**")
    print("------------------------")

    # 2. Show the identified frame
    show_common_frame(path1, idx1)

    # 3. Ask user for confirmation
    confirm = input("Confirm merge? (Y/N): ").strip().lower()
    if confirm != "y":
        print("Operation cancelled.")
        return

    # 4. Save merged file
    print("Trimming and merging clips...")
    output_filename = trim_and_merge(path1, path2, time1, time2)
    print(f"\nSuccess! Saved as {output_filename}")


if __name__ == "__main__":
    main()
