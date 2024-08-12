from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip


# Thoughts on how to tackle:
# First, I need a way to extract the end times of the next word
# Will need to use in range for loop
# Therefore, will have to make it not loop last word so that 
# ...index out of bound error does not occur


IMAGE_FOLDER = "C:\\Users\\blacb\\Desktop\\webImages\\"

def create_video(word_timestamps, audio):

    # Array of all the images
    all_image_segments = []

    # Minus 2 to prevent index out of bound error
    for i in range(0, len(word_timestamps)-2):

        # Need this so that the first clip starts at the start
        if i == 0:

            duration = word_timestamps[0][1] + (word_timestamps[1][1] - word_timestamps[0][1])

            image_segment = ImageClip(f"{IMAGE_FOLDER}0{word_timestamps[0][0]}.jpg").set_duration(duration)

            all_image_segments.append(image_segment)

            continue

        # Needed so that the last image lasts until the end of the audio clip  
        elif i == len(word_timestamps) - 2:

            pass
            continue

        duration = word_timestamps[i+1][1] - word_timestamps[i][1]

        image_segment = ImageClip(f"{IMAGE_FOLDER}{i}{word_timestamps[i][0]}.jpg").set_duration(duration)

        all_image_segments.append(image_segment)
    
    video = concatenate_videoclips(all_image_segments, method="compose")

    audio = AudioFileClip(audio)
    video = video.set_audio(audio)
    video.write_videofile("test_video.mp4", fps=24)



        
        
        
