from moviepy import editor
import os


def generate_video():
    # make this function of the length of the text video
    
    video = editor.VideoFileClip(os.path.dirname(__file__) + "/background_videos/parkour.mp4").subclip(0, 10)
    txt_clip = (
        editor.TextClip("abc", fontsize=70, color="white")
        .set_position("center")
        .set_duration(10)
    )
    
    result = editor.CompositeVideoClip([video, txt_clip]) # Overlay text on video
    result.write_videofile(os.path.dirname(__file__) +  "/completed_videos/test.mp4",fps=25) # Many options...


def main():
    generate_video()
