import streamlit as st
import subprocess
import os
import uuid
import requests
from movie import splice_video_selective_mute

# Function to generate audio from text
def generate_audio(text):
    url = "https://elevenlabsapi.vercel.app/api/media"
    data = {"name": f"{text}"}
    # aud = "".join(list(text.split(" "))) 

# Send the POST request
    response = requests.post(url, data=data)

# Check if the request was successful
    if response.status_code == 200:
        # Write the response content to a file
        with open("audio/audio.mp3", "wb") as f:
            f.write(response.content)
        print(f"Audio file saved as audio.mp3")
    else:
        print(f"Error: {response.status_code}, {response.text}")

   
    return "audio/audio.mp3"

# Function to run Wav2Lip command
def run_wav2lip(checkpoint_path, face_video, audio_file, output_file):
    command = [
        'python', 'inference.py',
        '--checkpoint_path', checkpoint_path,
        '--face', face_video,
        '--audio', audio_file,
        '--pads', '0', '20', '0', '0'
    ]
    result = subprocess.run(command)
    return result.returncode == 0

# Streamlit UI
st.title("Wav2Lip Automation")
name = st.text_input("Enter your name:")
if st.button("Generate Video"):
    if name:
        # Generate audio
        audio_file = generate_audio(name)
        st.info("Generating audio...")

        # Define paths
        checkpoint_path = "checkpoints/wav2lip_gan.pth"
        face_video = "test.mp4"
        output_file = "results/result_voice.mp4"
       

        # Display loading message
        with st.spinner("Generating video..."):
            success = run_wav2lip(checkpoint_path, face_video, audio_file, output_file) 
            
        if success:
            result = f"{name}.mp4"
            st.success("Video generated from voice successfully!")
            with st.spinner("Integrating into original video"):
                final = splice_video_selective_mute("test.mp4", output_file)
                final.write_videofile(f"{name}.mp4", codec='libx264', audio_codec='aac')
                final.close()
            st.success("Done!")
            st.balloons()    
            st.video(result)
            with open(result,'rb') as f:
                st.download_button(label='Download', data=f, file_name=f'{name}.mp4',mime="application/octet-stream")
            
        else:
            st.error("Error in video generation.")

        # Clean up temporary files
        os.remove(audio_file)
    else:
        st.warning("Please enter a name.")
