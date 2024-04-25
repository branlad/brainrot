import PIL.ImageDraw
from moviepy import editor
import os
from gtts import gTTS
from pydub import AudioSegment
import PIL
import ffmpeg

PATH = os.path.dirname(__file__)


def get_post():
    title = "This is a title"
    content = """1 This is the content of the post 2 This is the content of the post 3 This is the content of the post 4 This is the content of the post 5 This is the content of the post
    6 This is the content of the post
    7 This is the content of the post
    """
    return title, content


def generate_text(words, index):
    image = PIL.Image.new("RGBA", (800, 600), (0, 0, 0, 0))
    draw = PIL.ImageDraw.Draw(image)
    draw.text(words, fill="white")
    image.save(PATH + f"/videos/text_files/line{index}.png")


def generate_tts():
    title, content = get_post()

    tts = gTTS(content, lang="en", slow=False)
    tts.save(PATH + "/videos/audio_files/hello_world.mp3")
    audio_length = (
        len(AudioSegment.from_file(PATH + "/videos/audio_files/hello_world.mp3")) / 1000
    )

    return audio_length


def generate_video():
    # make this function of the length of the text video
    audio_length = generate_tts()

    video = editor.VideoFileClip(
        PATH + "/videos/background_videos/parkour.mp4"
    ).subclip(0, audio_length)
    txt_clip = (
        editor.TextClip("abc", fontsize=70, color="white")
        .set_position("center")
        .set_duration(10)
    )

    result = editor.CompositeVideoClip([video, txt_clip])  # Overlay text on video
    result.write_videofile(
        PATH + "/videos/completed_videos/test.mp4", fps=25
    )  # Many options...


def main():
    generate_video()
