import os

from moviepy import VideoFileClip, concatenate_videoclips


def trim_and_merge(path1, path2, time1, time2):
    clip1 = VideoFileClip(path1)
    clip2 = VideoFileClip(path2)

    final_clip1 = clip1.subclipped(0, time1)
    final_clip2 = clip2.subclipped(time2, clip2.duration)

    final_video = concatenate_videoclips([final_clip1, final_clip2])

    name1 = os.path.splitext(os.path.basename(path1))[0]
    name2 = os.path.splitext(os.path.basename(path2))[0]
    output_filename = f"{name1}_{name2}.mp4"
    final_video.write_videofile(output_filename, codec="libx264", audio_codec="aac")

    clip1.close()
    clip2.close()

    return output_filename
