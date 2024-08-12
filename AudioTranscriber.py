import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks
from Tokenise import extract_keywords
from GrabImages import get_images

# Define constants
AUDIO_FILE = "Dogs.wav"
CHUNK_LENGTH_MS = 5000  # Length of each chunk in milliseconds
OVERLAP_MS = 1000  # Overlap between chunks in milliseconds


def get_timestamps_for_keywords(audio_file):
    # Load the audio file with speech recognition
    audio = AudioSegment.from_file(audio_file)
    
    # Split audio into chunks with overlap using pydub
    chunks = make_chunks(audio, CHUNK_LENGTH_MS - OVERLAP_MS)

    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Uses the audio file as a source for audio
    with sr.AudioFile(audio_file) as source:
        recognizer.adjust_for_ambient_noise(source)
        audio2 = recognizer.record(source)

    # This transcribes the audio fully, then outputs the keywords
    try:
        full_transcription = recognizer.recognize_google(audio2).lower()
        keywords = extract_keywords(full_transcription)
    except Exception as e:
        print("Cant transcribe: ", e)

    # Track timestamps
    word_timestamps = []

    # Transcribe each chunk
    # Enumerate allows us to have an index (i) and the actual value (chunk)
    # The reason we use chunks is to make it easier for the file to be processed
    # This is especially good for dealing with really long audio files, where the processor can be overloaded
    for i, chunk in enumerate(chunks):
        with sr.AudioFile(chunk.export(format="wav")) as source:
            audio_data = recognizer.record(source)

            try:
                # Transcribe the chunk
                transcription = recognizer.recognize_google(audio_data).lower()

                # Calculate start time for the chunk to see which chunk the audio is a part of
                start_time_ms = max(0, i * (CHUNK_LENGTH_MS - OVERLAP_MS))

                # Debug: Output the transcription of each chunk
                print(f"Chunk {i}: {transcription}")

                # Search for keywords and calculate timestamps
                for keyword in keywords:
                    if keyword in transcription:
                        # Estimate position in chunk
                        word_index = transcription.index(keyword)
                        # Estimate time position in milliseconds
                        keyword_time_ms = start_time_ms + int((word_index / len(transcription)) * len(chunk))
                        word_timestamps.append((keyword, keyword_time_ms))
                        print(f"Keyword '{keyword}' found at {keyword_time_ms}ms")

            except sr.UnknownValueError:
                print(f"Chunk {i}: Could not understand audio")
            except sr.RequestError as e:
                print(f"Error with the speech recognition service: {e}")
                return

    # Output the results
    print("\nTimestamps for specified keywords:")
    for word, timestamp in word_timestamps:
        print(f"{word}: {timestamp}ms")
    
    return word_timestamps

# Get timestamps for specified keywords
word_timestamps = get_timestamps_for_keywords(AUDIO_FILE)

for word in word_timestamps:
    get_images(word[0])
