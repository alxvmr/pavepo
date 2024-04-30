from . import s3, text_module

path_video = r"C:\Users\alexe\Desktop\pavepo\temp\vid2.mp4"

name = s3.upload_object(path_video)
name = text_module.get_audio_from_video(name)
text_module.audio_2_text(name)