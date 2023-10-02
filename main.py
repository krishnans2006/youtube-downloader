from pytube import YouTube
from moviepy.editor import AudioFileClip
from mutagen.easyid3 import EasyID3


URL = "https://youtu.be/dQw4w9WgXcQ"

video = YouTube(URL)

print(video.title)
print(video.metadata)

streams = video.streams

audio = streams.get_audio_only()

audio.download(filename="temp.mp4")

audio_mp4 = AudioFileClip("temp.mp4")
audio_mp4.write_audiofile("video.mp3")

audio_mp3 = EasyID3("video.mp3")
audio_mp3["title"] = video.title
audio_mp3["artist"] = video.author
audio_mp3.save()
