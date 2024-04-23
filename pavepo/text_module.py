# извлечение текста из видео
from . import s3
import moviepy.editor as mpe
import os

def get_audio_from_video(video_name, bucket=None):
    # Получение зука из видео
    video = None
    # Получение видео из хранилища по API
    if not bucket:
        video = s3.get_object(video_name)["Body"]
    else:
        video = s3.get_object(video_name, bucket=bucket)["Body"]
    if video:
        presignedurl = s3.create_presigned_url(video_name)
        audioclip = mpe.AudioFileClip(presignedurl)
        # сохранение аудиодорожки в хранилище
        path_audio = f"./temp/{video_name}_audio.mp3"
        audioclip.write_audiofile(path_audio)
        s3.upload_object(path_audio)
        # удаление из локального хранилища
        os.remove(path_audio)
        return audioclip
    return None


def get_text_from_video(video_name, bucket=None):
    # Получение звука из видео
    audioclip = get_audio_from_video(video_name, bucket)
        

if __name__ == "__main__":
    get_text_from_video("vid2.mp4")