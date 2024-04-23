# извлечение текста из видео
from . import s3
import moviepy.editor as mpe

def get_video(video_name, bucket=None):
    # Получение видео из хранилища по API
    video = None
    # Получение видео из хранилища по API
    if not bucket:
        video = s3.get_object(video_name)["Body"]
    else:
        video = s3.get_object(video_name, bucket=bucket)["Body"]
    if video:
        presignedurl = s3.create_presigned_url(video_name)
        vidclip = mpe.VideoFileClip(presignedurl)
        return vidclip
    return None


def get_text_from_video(video_name, bucket=None):
    # Получение текста из видео
    video = get_video(video_name, bucket)
    video.preview(fps=20)
        

if __name__ == "__main__":
    get_text_from_video("vid2.mp4")