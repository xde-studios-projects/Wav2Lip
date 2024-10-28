from moviepy.editor import VideoFileClip, CompositeVideoClip, concatenate_audioclips

# Load the main video
main_video = VideoFileClip("test.mp4")

# Load the overlay video
overlay_video = VideoFileClip("results/result_voice.mp4")

# Specify the start time for the overlay video
start_time = 0.3

# Resize the overlay video to match the dimensions of the main video
overlay_video = overlay_video.resize(main_video.size)

# Extract the original audio from the main video
main_audio = main_video.audio

# Create a new audio clip that mutes the main audio during the overlay duration
overlay_duration = overlay_video.duration

# Get the audio before the overlay
audio_before_overlay = main_audio.subclip(0, start_time)

# Get the audio after the overlay
audio_after_overlay = main_audio.subclip(start_time + overlay_duration, main_video.duration)

# Combine audio clips: before overlay and after overlay
final_audio = concatenate_audioclips([audio_before_overlay, audio_after_overlay])

# Create a composite video
final_video = CompositeVideoClip([main_video, overlay_video.set_start(start_time)])

# Set the new audio to the final video
final_video.set_audio(final_audio)

# Write the final video to a new file
final_video.write_videofile("final_output_video.mp4", codec='libx264', audio_codec='aac')
