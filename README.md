# multi-speaker-demo
Convert a podcast script into audio

## Usage
- Install ffmpeg on host, e.g. `apt install update && apt install ffmpeg`
- Create and enable virtualenv: `virtualenv venv && . venv/bin/activate`
- Install Python dependencies: `pip install -r requirements.txt`
- Run code: `python podcast.py`

## Configuration Options
- List of voices available: https://cloud.google.com/text-to-speech/docs/chirp3-hd#chirp3-hd-voice-controls
- Audio encoding options: https://cloud.google.com/python/docs/reference/texttospeech/latest/google.cloud.texttospeech_v1.types.AudioEncoding
  - Make sure to update any usage of pydub's AudioSegment in podcast.py 
