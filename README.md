# Development of a mention and sentiment detection platform
*The ```pavepo/main.py``` file is the start of the program.

## OLTP layer
The ```vk cloud``` object storage was chosen as the data storage platform.
All access data is stored in an ```.env``` file
All intermediate and final results are stored in the cloud.

## Text extraction module from video
The ```moviepy```, ```pydub``` and ```speech_recognition``` stack was used.
The source video, extracted audio and recognized text are stored in object storage
To work with pydub, the audio and chunks are stored locally, once they are processed and sent to the repository, the local files are deleted.

