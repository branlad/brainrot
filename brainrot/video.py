from moviepy import editor
import os
from gtts import gTTS
import assemblyai as aai
from dotenv import load_dotenv
import pysrt
import math

PATH = os.path.dirname(__file__)

TTS_AUDIO_PATH = PATH + "/videos/audio_files/tts_audio.mp3"
SRT_FILE_PATH = PATH + "/videos/audio_files/subtitles.srt"


def get_post():
    title = "This is a title"
    content = "This is"

    return title, content


def create_tts_mp3_file():
    title, content = get_post()

    tts = gTTS(content, lang="en", slow=False)
    tts.save(TTS_AUDIO_PATH)


def create_srt_file():
    load_dotenv()
    aai.settings.api_key = os.getenv("ASSEMBLYAI_KEY")
    transcript = aai.Transcriber().transcribe(TTS_AUDIO_PATH)

    for i in range(1, 10):
        try:
            srt = transcript.export_subtitles_srt(chars_per_caption=(5 * i))
            break
        except Exception:
            continue

    with open(SRT_FILE_PATH, "w") as f:
        f.write(srt)


def get_subtitle_clips(subtitles):
    clips = []
    for sub in subtitles:
        txt_clip = editor.TextClip(
            sub.text,
            fontsize=100,
            color="white",
            stroke_color="black",
            stroke_width=0.5,
        )
        txt_clip = txt_clip.set_start(sub.start.ordinal / 1000.0).set_duration(
            (sub.end - sub.start).ordinal / 1000.0
        )
        txt_clip = txt_clip.set_pos("center")

        clips.append(txt_clip)

    return clips


def combine_audio_files(video):
    tts_voice = editor.AudioFileClip(TTS_AUDIO_PATH)
    # background_music = editor.AudioFileClip(PATH + "/videos/audio_files/background_music.mp3")

    audio = editor.concatenate_audioclips([tts_voice])
    return video.set_audio(audio)


def crop_video(video):
    video = video.resize(height=1920)

    if video.size[0] > 1080:
        video = video.crop(x_center=video.size[0] / 2, width=1080)

    return video


def create_video():
    subtitles = pysrt.open(SRT_FILE_PATH)
    video = editor.VideoFileClip(
        PATH + "/videos/background_videos/parkour.mp4"
    ).subclip(0, math.ceil(subtitles[-1].end.ordinal / 1000.0))

    video = crop_video(combine_audio_files(video))

    result = editor.CompositeVideoClip(
        [video] + get_subtitle_clips(subtitles)
    )
    result.write_videofile(PATH + "/videos/completed_videos/increment_this.mp4", fps=25)


def get_video():
    create_tts_mp3_file()
    create_srt_file()
    create_video()
