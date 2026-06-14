# # convert videos to mp3 

# METHOD 1: Using moviepy library

# import os
# import subprocess
# def convert_video_to_mp3(video_path, output_path):
#     command = f"ffmpeg -i {video_path} -q:a 0 -map a {output_path}"
#     subprocess.run(command, shell=True)
# if __name__ == "__main__":
#     video_path = "input_video.mp4"  # replace with your video path -> C:\Users\ASUS\Downloads\RAG_Based_AI\Videos
#     output_path = "output_audio.mp3"  # replace with your desired output path -> C:\Users\ASUS\Downloads\RAG_Based_AI\Audio
#     convert_video_to_mp3(video_path, output_path)


# Method 2: Using ffmpeg command line tool

import os
import subprocess

files = os.listdir("Videos")
for file in files:
    file_number = file.split(".")[0] 
    file_name = file.split(".")[1]
    print(file_number, file_name)

    subprocess.run(["ffmpeg", "-i", f"Videos/{file}", f"Audio/{file_number}_{file_name}.mp3"])
