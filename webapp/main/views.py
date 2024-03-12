from django.shortcuts import render

from django.shortcuts import render

from django.core.files.storage import FileSystemStorage
import os

from moviepy.video.io.VideoFileClip import VideoFileClip

os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"
from SemanticVoiceAnalysis import *
import subprocess

counter = 0


def home(request):
    FileSystemStorage().delete('speech_video.mp4')
    FileSystemStorage().delete('myprosody/dataset/audioFiles/speech_audio.wav')
    FileSystemStorage().delete('myprosody/dataset/audioFiles/speech_audio.textgrid')
    request.session.flush()
    if request.method == "POST":
        request_file = request.FILES.get('document')
        if request_file:
            if request_file.name.lower().endswith('.mp4'):
                fs = FileSystemStorage()
                file = fs.save('speech_video.mp4', request_file)
                fileurl = fs.url(file)
                return main_summary(request)
            else:
                return render(request, 'uploadFile.html', {'error': 'Invalid file format'})
    return render(request, 'uploadFile.html', {})



def main_summary(request):
    fs = FileSystemStorage()

    if 'df' not in request.session:
        video_path = fs.path('speech_video.mp4')
        video = VideoFileClip(video_path)
        audio_path = '/Users/nipun/PycharmProjects/VoiceBox/webapp/media/myprosody/dataset/audioFiles/speech_audio.wav'
        video.audio.write_audiofile(audio_path)
        df = voiceAnalysis(r'speech_audio')

        request.session['df'] = df.to_json()
        request.session.save()
    else:
        json_string = request.session['df']
        df = pd.read_json(json_string)


    context = {'speakingpercentage': str(speakingPercentage(df)), 'rate_of_speech': str(df.loc['rate_of_speech'][0]),
               'articulation_rate': str(df.loc['articulation_rate'][0]), 'gender': str(df.loc['gender'][0]),
               'intonation': str(df.loc['intonation'][0]), 'number_of_pauses': str(df.loc['number_of_pauses'][0])}
    print(df)
    return render(request, 'main-summary.html', context)

