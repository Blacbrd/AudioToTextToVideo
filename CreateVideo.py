from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
import pydub
import math


# Thoughts on how to tackle:
# First, I need a way to extract the end times of the next word
# Will need to use in range for loop
# Therefore, will have to make it not loop last word so that 
# ...index out of bound error does not occur


IMAGE_FOLDER = "C:\\Users\\blacb\\Desktop\\webImages\\"


def get_audio_duration(audio):

    audio = pydub.AudioSegment.from_file(audio)
    audio_duration = len(audio)
    return audio_duration


def create_video(word_timestamps, audio):

    all_image_segments = []
    
    print(word_timestamps)
    # Pre-handles all the durations of the image segments
    durations = [
        word_timestamps[i+1][1] - word_timestamps[i][1]
        for i in range(len(word_timestamps) - 1)
    ]

    durations_sec = [

        (durations[i] / 1000)
        for i in range(len(durations))

    ]

    print(durations_sec)
    
    # Handle the first image separately to start the video
    first_duration = (word_timestamps[0][1] + durations[0]) / 1000
    first_image_segment = ImageClip(f"{IMAGE_FOLDER}0_{word_timestamps[0][0]}.jpg").set_duration(first_duration)
    all_image_segments.append(first_image_segment)

    print(first_duration)
    
    last_image_number = 1

    # Handle the rest of the images, excluding the last one
    for i in range(1, len(durations_sec)):
        print("You are inside")
        image_segment = ImageClip(f"{IMAGE_FOLDER}{i}_{word_timestamps[i][0]}.jpg").set_duration(durations_sec[i])
        all_image_segments.append(image_segment)
        last_image_number += 1

        print(f"{IMAGE_FOLDER}{i}_{word_timestamps[i][0]}.jpg")
        print(last_image_number)
    
    # How long the final image should last
    last_duration = (get_audio_duration(audio) - word_timestamps[last_image_number][1]) / 1000
    last_image_segment = ImageClip(f"{IMAGE_FOLDER}{last_image_number}_{word_timestamps[last_image_number][0]}.jpg").set_duration(last_duration)
    all_image_segments.append(last_image_segment)

    print(last_duration)
    
    # Concatenate video clips
    video = concatenate_videoclips(all_image_segments, method="compose")
    
    # Attach audio
    audio_clip = AudioFileClip(audio)
    video = video.set_audio(audio_clip)
    
    try:
        # Write the final video file
        video.write_videofile("test_video.mp4", threads=16, fps=24)
    
    except Exception as e:

        print(e)







        
        
        
