from moviepy import editor
import os
from gtts import gTTS
import assemblyai as aai
from dotenv import load_dotenv
import pysrt
import math

from elevenlabs import client, save

from datetime import timedelta
import srt
import shutil

PATH = os.path.dirname(__file__)

TTS_AUDIO_PATH = PATH + "/videos/audio_files/tts_audio.mp3"
SRT_FILE_PATH = PATH + "/videos/audio_files/subtitles.srt"
BRAINROT_PATH = PATH + "/videos/completed_videos/brainrot.mp4"


def verify_file_paths():
    os.makedirs(os.path.dirname(TTS_AUDIO_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(SRT_FILE_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(BRAINROT_PATH), exist_ok=True)


def create_tts_mp3_file(content):


    # eleven_client = client.ElevenLabs(api_key=os.getenv("ELEVENLABS_KEY"))
    # audio = eleven_client.generate(
    #     text=content, voice="Antoni", model="eleven_multilingual_v2"
    # )
    # save(audio=audio, filename=TTS_AUDIO_PATH)

    tts = gTTS(content, lang="en", slow=True)
    tts.save(TTS_AUDIO_PATH)

    return content
    
    
# def create_srt_file(content):
#     load_dotenv()
#     aai.settings.api_key = os.getenv("ASSEMBLYAI_KEY")
#     transcript = aai.Transcriber().transcribe(TTS_AUDIO_PATH)

#     for i in range(1, 10):
#         try:
#             srt_data = transcript.export_subtitles_srt(chars_per_caption=(5 * i))
#             break
#         except Exception:
#             continue

#     subtitles = [s for s in pysrt.from_string(srt_data) if s.end.ordinal / 1000.0 <= 60]
#     srt_data = '\n\n'.join(str(s) for s in subtitles)
    
#     with open(SRT_FILE_PATH, "w") as f:
#         f.write(srt_data) 
  

    
    
def create_srt_file(content):
    load_dotenv()
    aai.settings.api_key = os.getenv("ASSEMBLYAI_KEY")
    transcript = aai.Transcriber().transcribe(TTS_AUDIO_PATH)
    total_audio_duration = transcript.words[-1].end + 1

    recognized_words = [word for word in transcript.words if word.confidence > 0.5]
    recognized_timings = [word.end for word in recognized_words]

    full_words = content.split()
    subtitles = []
    for i, word in enumerate(full_words):
        if word in recognized_words:
            timing = recognized_timings[recognized_words.index(word)]
        else:
            timing = (i / len(full_words)) * total_audio_duration

        subtitle = srt.Subtitle(index=i, start=timedelta(seconds=timing), end=timedelta(seconds=timing + 1), content=word)
        subtitles.append(subtitle)

    srt_data = srt.compose(subtitles)
    
    with open(SRT_FILE_PATH, "w") as f:
        f.write(srt_data)
        
    shutil.copy(SRT_FILE_PATH, SRT_FILE_PATH + "1")


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
    tts_voice = tts_voice.subclip(0, min(60, tts_voice.duration))
    tts_voice = tts_voice.subclip(0, min(60, tts_voice.duration))
    # background_music = editor.AudioFileClip(PATH + "/videos/audio_files/background_music.mp3")

    audio = editor.concatenate_audioclips([tts_voice])
    return video.set_audio(audio)


def crop_video(video):
    video = video.resize(height=1920)

    if video.size[0] > 1080:
        video = video.crop(x_center=video.size[0] / 2, width=1080)

    return video


def create_video():
    subtitles = pysrt.open(SRT_FILE_PATH + "1")
    video = editor.VideoFileClip(
        PATH + "/videos/background_videos/parkour.mp4"
    ).subclip(0, min(60, math.ceil(subtitles[-1].end.ordinal / 1000.0)))
    video = crop_video(combine_audio_files(video))

    result = editor.CompositeVideoClip([video] + get_subtitle_clips(subtitles))
    result.write_videofile(BRAINROT_PATH, fps=25)


class Post:
    def __init__(self, title, text):
        self.title = title
        self.text = text


def get_video():
    post = Post("hello world", "will this work as expected??")
    content = post.title + " " + post.text
    limited_content = " ".join(content.split(" ")[:200])
    
    verify_file_paths()
    create_tts_mp3_file(limited_content)
    create_srt_file(limited_content)
    create_video()
