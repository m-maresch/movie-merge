# movie-merge

`movie-merge` is a simple command-line tool that merges two video files (including audio) with overlapping content by automatically identifying a common "bridge" frame. Instead of manually scrubbing through timelines to find a cut point, `movie-merge` scans both files, finds the best visual match, and handles the trimming and concatenation.

## Usage

Run the tool by passing the paths to your two video files. Video 1 will be the "start" and Video 2 will be the "end".

```
./movie_merge.sh ./video1.mp4 ./video2.mp4
```

## Installation

Clone the repository:

```
git clone https://github.com/m-maresch/movie-merge
cd movie-merge
```

Install dependencies in Python venv:

```
python -m venv .
source bin/activate
pip install opencv-python tqdm moviepy
```

## Workflow

1. Indexing: The tool creates a visual index of Video 1.
2. Scanning: It searches Video 2 for a common frame.
3. Preview: A window opens showing the identified, common frame.
4. Confirmation by the user whether or not to continue: Yes/No
5. Render: If confirmed, the tool trims the videos as needed and exports a .mp4 file.

To prevent incorrect merges on e.g. black frames, `movie-merge` employs a contrast-aware filter. It automatically ignores frames with low variance or near-zero brightness, ensuring the tool anchors onto "real" visual content.

## Performance Tuning

You can narrow the search to specific timestamps to save time:

- `--start-at-min`: Only index Video 1 starting from this minute.
- `--end-at-min`: Only scan Video 2 up until this minute.

**Example:**

```
./movie_merge.sh video1.mp4 video2.mp4 --start-at-min 20 --end-at-min 1
```

Scanning every single frame of a video is computationally expensive. The `-n` flag can be used to adjust the sampling rate:

| Command | Behavior | Outcome |
| :--- | :--- | :--- |
| `./movie_merge.sh video1.mp4 video2.mp4 -n 1` | Sample every frame (default) | Maximum precision, slow. |
| `./movie_merge.sh video1.mp4 video2.mp4 -n 10` | Sample every 10th frame | Balance of speed/accuracy. |

## License

This project is licensed under the MIT License. See the `LICENSE.txt` file for details. Third-party library notices are documented in `THIRD-PARTY-NOTICES.txt`.

## Acknowledgments

This project was developed with the assistance of Google Gemini 3.

## Dependencies

Thanks to everyone contributing to any of the following projects:

- OpenCV
- MoviePy
- NumPy
- tqdm
