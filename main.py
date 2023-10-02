import argparse
import os

from pytube import YouTube
from moviepy.editor import AudioFileClip
from mutagen.easyid3 import EasyID3


def get_filename(video, filename):
    if not filename:
        filename = "".join(c if c.isalnum() else "_" for c in video.title)

    return filename


def get_filepath(filename, temp=False):
    return os.path.join(os.getcwd(), "temp" if temp else "out", filename)


def get_video(url):
    video = YouTube(url)
    return video


def get_audio_stream(url):
    video = YouTube(url)
    stream = video.streams.get_audio_only()
    return stream


def download_mp4(stream, filename):
    stream.download(filename=get_filepath(filename, temp=True) + ".mp4")
    return filename


def mp4_to_mp3(filename):
    temp_filepath = get_filepath(filename, temp=True)
    out_filepath = get_filepath(filename)
    audio_mp4 = AudioFileClip(temp_filepath + ".mp4")
    audio_mp4.write_audiofile(out_filepath + ".mp3")


def set_metadata(filename, video, title, artist, album):
    filepath = get_filepath(filename)

    audio_mp3 = EasyID3(filepath + ".mp3")
    if title:
        audio_mp3["title"] = title
    else:
        audio_mp3["title"] = video.title
    if artist:
        audio_mp3["artist"] = artist
    else:
        audio_mp3["artist"] = video.author
    if album:
        audio_mp3["album"] = album
    else:
        pass
    audio_mp3.save()


def main(args):
    video = get_video(args.url)
    filename = get_filename(video, args.filename)

    audio_stream = get_audio_stream(args.url)
    download_mp4(audio_stream, filename)

    mp4_to_mp3(filename)

    set_metadata(filename, video, args.title, args.artist, args.album)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="URL of the video to download", required=True)
    parser.add_argument(
        "-f", "--filename", help="Filename to download to, excluding file extension"
    )

    metadata = parser.add_argument_group("metadata options", "Override audio metadata")
    metadata.add_argument("-t", "--title", help="Song title")
    metadata.add_argument("-a", "--artist", help="Song artist")
    metadata.add_argument("-A", "--album", help="Song album")

    main(parser.parse_args())
