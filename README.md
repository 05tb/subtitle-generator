# Subtitle Generator

Use Whisper and FFmpeg to automatically generate subtitles and add them to a video file.

Inspired by - https://www.digitalocean.com/community/tutorials/how-to-generate-and-add-subtitles-to-videos-using-python-openai-whisper-and-ffmpeg

## Requirements

* Python 3
* FFmpeg - https://www.ffmpeg.org

## Install Instructions

* Move into the cloned repo directory `cd generate-subtitles`
* Create a virtual environment `python3 -m venv .venv`
* Active the virtual environment `source .venv/bin/activate`
* Install the Python requirements `python3 -m pip install -r requirements.txt`

## Using

A command line interface is provided for convenience. Help is available:

```python3 main.py --help```

### Generate Subs

If you have a video file and would like to generate subtitles use the following command
```python3 main.py generatesubs video.mp4```

### Add Subs

If you have a subtitle file and would like to add it to a video use the following command
```python3 main.py addsubs video.mp4 subtitles.srt```

Optional variables can be added
```python3 main.py addsubs video.mp4 subtitles.srt soft_subtitle=False subtitle_language="en"```

* set `soft_subtitle=False` for burnt in subtitles, the default option
* set `soft_subtitle=True` to embed a subtitle file into the video, letting the video player decide the subtitle formatting
