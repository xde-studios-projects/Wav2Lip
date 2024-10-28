from moviepy.editor import VideoFileClip, concatenate_videoclips


def splice_video_selective_mute(original_path, new_path, splice_time=0.75):
    # Load the videos
    original = VideoFileClip(original_path)
    new_clip = VideoFileClip(new_path)

    # Get the duration of the new clip
    new_clip_duration = new_clip.duration

    # Split the original video into three parts:
    # 1. Before splice point (with audio)
    # 2. During new clip duration (muted)
    # 3. After new clip ends (with audio)
    first_part = original.subclip(0, splice_time)

    # This part will be muted as it would overlap with new clip
    overlapping_part = original.subclip(splice_time, splice_time + new_clip_duration).without_audio()

    # The remaining part keeps its audio
    remaining_part = original.subclip(splice_time + new_clip_duration)

    # Concatenate all parts
    final_video = concatenate_videoclips([
        first_part,  # Original video with audio until splice point
        new_clip.speedx(1.25),  # New video with its audio
        remaining_part  # Rest of original video with audio
    ])

    return final_video
