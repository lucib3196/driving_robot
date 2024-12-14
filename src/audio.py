from pathlib import Path
from openai import OpenAI
client = OpenAI()

speech_file_path = Path(__file__).parent / "speech.mp3"
response = client.audio.speech.create(
  model="tts-1",
  voice="echo",
  input="Yo, check it out! We're looking at a glorious mess of code and whatever this wild desktop scenario is. I mean, damn, is that a coding party I see? Code snaking all over the place like it’s trying to escape!\n\nBut seriously, lock in for a second. I hope you’re ready to sift through this digital chaos. Dammmm that crazzzzyyyy! What are we—building a spaceship? A website to sell cat memes? Either way, let’s go!"
)

response.stream_to_file(speech_file_path)