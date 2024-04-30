# извлечение текста из видео
from . import s3
import moviepy.editor as mpe
import os
import shutil
import speech_recognition as sr
import pydub
from pydub import AudioSegment
from pydub.silence import split_on_silence 

pydub.AudioSegment.ffmpeg = "ffmpeg.exe"
TEMP_PATH = "./temp/"


def mp3_2_wav(path_audio, save_path):
    save_path =os.path.join(os.getcwd(), save_path)
    sound = AudioSegment.from_mp3(path_audio)
    sound.export(save_path, format="wav")


def get_audio_from_video(video_name, bucket=None):
    # Получение видео из хранилища по API
    presignedurl = s3.create_presigned_url(video_name)
    audioclip = mpe.AudioFileClip(presignedurl)
    # сохранение аудиодорожки в хранилище
    path_audio_mp3 = os.path.join(TEMP_PATH, f"{video_name}_audio.mp3")
    print(path_audio_mp3)
    path_audio_wav = os.path.join(TEMP_PATH, f"{video_name}_audio.wav")
    audioclip.write_audiofile(path_audio_mp3)
    mp3_2_wav(path_audio_mp3, path_audio_wav)
    name = s3.upload_object(path_audio_wav)
    # удаление из локального хранилища
    print(path_audio_mp3)
    os.remove(path_audio_mp3)
    return name


# нормализация чанка по амплитуде
def match_target_amplitude(aChunk, target_dBFS):
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)

def audio_2_text(name, bucket=None): 
    audio_wav_path = os.path.join(TEMP_PATH, name)
    audio = AudioSegment.from_wav(audio_wav_path)
    os.remove(audio_wav_path)

    chanks_dir = f'./temp/audio_chunks_{name}'
    # создание локальной директории для хранения чанков
    try: 
        os.mkdir(chanks_dir) 
    except(FileExistsError): 
        pass
    name_save = f"{chanks_dir}/{name}_recognized.txt"

    fh = open(name_save, "w+") 

    # разбиение записи на чанки
    chunks = split_on_silence(audio, 
        min_silence_len = 2000, 
        silence_thresh = -16,
        keep_silence=200
    )

    os.chdir(chanks_dir)

    for i, chunk in enumerate(chunks):
        # создание паддинга тишины
        silence_chunk = AudioSegment.silent(duration=1000)
        audio_chunk = silence_chunk + chunk + silence_chunk

        # нормализация чанка
        normalized_chunk = match_target_amplitude(audio_chunk, -20.0)

        filename = f"chunk{i}.wav"

        # экспорт с новым битрейтом
        print(f"Exporting chunk{i}")
        normalized_chunk.export(
            filename, 
            bitrate ='192k', 
            format ="wav"
            ) 
        
        r = sr.Recognizer() 
  
        with sr.AudioFile(filename) as source: 
            r.adjust_for_ambient_noise(source)
            audio_listened = r.listen(source)
  
        try: 
            rec = r.recognize_google(audio_listened, language = 'ru-RU', show_all = True)
            fh.write(rec['alternative'][0]['transcript']+" ") 
  
        except sr.UnknownValueError: 
            print("Could not understand audio") 
  
        except sr.RequestError as e: 
            print("Could not request results. Check your internet connection")

    fh.close()
    os.chdir('../..')
    # отправка расшифрованного файла в объектное хранилище
    s3.upload_object(name_save, bucket)

    # удаление локальной директории с чанками
    shutil.rmtree(chanks_dir)


if __name__ == "__main__":
    #C:/Users/alexe/Desktop/pavepo/temp/vid2.mp4
    get_audio_from_video("vid2.mp4")
    # разделить по точкам и отбросить последний кусок