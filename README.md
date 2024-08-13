# AudioToTextToVideo
Transcribes text, scrapes the web, then makes a video

This is a project I worked on during the 2024 Summer before going to university. I initially got the idea from how some YouTube content would have people talking to the camera, accompanied by various images relating to what they were saying.

Synopsis of what the program does:

* Allows user to input file in variable
* Audio file is transcribed
* Transcription is run through Python's NLTK, which removes all the stopwords and tokenises the words
* Tokenised words ran through transcription program to estimate where they appear in the audio (achieved through audio chunking)
* Tokenised words are taken and a selenium web scraper searches for the images and downloads them
* Once images are downloaded, they are compiled into a video with the audio

So far, the program has these issues:

* The image scraping takes a really really long time
* The image time stamps don't appear exactly where the word is said

