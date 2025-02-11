import math
import ffmpeg
import fire

from faster_whisper import WhisperModel


#https://www.digitalocean.com/community/tutorials/how-to-generate-and-add-subtitles-to-videos-using-python-openai-whisper-and-ffmpeg


def extract_audio(input_video):
    extracted_audio = f"audio-{input_video}.wav"
    stream = ffmpeg.input(input_video)
    stream = ffmpeg.output(stream, extracted_audio)
    ffmpeg.run(stream, overwrite_output=True)
    return extracted_audio


def transcribe(audio):
    model = WhisperModel("small")
    segments, info = model.transcribe(audio)
    language = info.language
    print("Transcription language", language)
    segments = list(segments)
    for segment in segments:
        # print(segment)
        print("[%.2fs -> %.2fs] %s" %
              (segment.start, segment.end, segment.text))
    return language, segments


def format_time(seconds):
    hours = math.floor(seconds / 3600)
    seconds %= 3600
    minutes = math.floor(seconds / 60)
    seconds %= 60
    milliseconds = round((seconds - math.floor(seconds)) * 1000)
    seconds = math.floor(seconds)
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:01d},{milliseconds:03d}"
    return formatted_time


def generate_subtitle_file(input_video, language, segments):
    subtitle_file = f"sub-{input_video}.{language}.srt"
    text = ""
    for index, segment in enumerate(segments):
        segment_start = format_time(segment.start)
        segment_end = format_time(segment.end)
        text += f"{str(index+1)} \n"
        text += f"{segment_start} --> {segment_end} \n"
        text += f"{segment.text} \n"
        text += "\n"
        
    f = open(subtitle_file, "w")
    f.write(text)
    f.close()
    return subtitle_file


def generateSubs(input_video):

    """
    Generate an .srt file from a video

    Args:
        input_video (str): path to a media file
    """    

    extracted_audio = extract_audio(input_video)
    language, segments = transcribe(audio=extracted_audio)
    subtitle_file = generate_subtitle_file(
        input_video,
        language=language,
        segments=segments
    )


def add_subtitle_to_video(input_video, subtitle_file, soft_subtitle=False, subtitle_language="eng"):

    """
    Add an existing .srt subtitle file to a video, either as an embedded file or burnt in

    Args:
        input_video (str): path to a media file
        subtitle_file (str): path to a .srt file
        soft_subtitle (bool, optional): defaults to False, generating burnt it subtitles
        subtitle_language (str, optional): defaults to 'eng' for English language 
    """    

    video_input_stream = ffmpeg.input(input_video)
    subtitle_input_stream = ffmpeg.input(subtitle_file)
    output_video = f"output-{input_video}.mp4"
    subtitle_track_title = subtitle_file.replace(".srt", "")

    if soft_subtitle:
        stream = ffmpeg.output(
            video_input_stream, subtitle_input_stream, output_video, **{"c": "copy", "c:s": "mov_text"},
            **{"metadata:s:s:0": f"language={subtitle_language}",
            "metadata:s:s:0": f"title={subtitle_track_title}"}
        )
        ffmpeg.run(stream, overwrite_output=True)
    else:
        stream = ffmpeg.output(video_input_stream, output_video,

                               vf=f"subtitles={subtitle_file}")

        ffmpeg.run(stream, overwrite_output=True)


fire.Fire({
    "generatesubs" : generateSubs,
    "addsubs" : add_subtitle_to_video
})