from django.http import HttpResponse
from pydub import AudioSegment

from django.shortcuts import render

from django.core.files.storage import FileSystemStorage
import os

from moviepy.video.io.VideoFileClip import VideoFileClip
#TODO: download ffmpeg and change the path if necessary
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"
from SemanticVoiceAnalysis import *
from SemanticContentAnalysis import *
from Loudness import *
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
        #TODO: change the path to the audio file
        audio_path = '/Users/nipun/PycharmProjects/VoiceBox/webapp/media/myprosody/dataset/audioFiles/speech_audio.wav'
        video.audio.write_audiofile(audio_path)
        df = voiceAnalysis(r'speech_audio')
        content_dict = get_statistics(audio_path)
        new_df = pd.DataFrame(content_dict.values(), index=content_dict.keys())
        df = pd.concat([df, new_df])
        df.loc['Spikes'] = [len(volumeSpikes(audio_path))]
        df.loc['Dips'] = [len(volumeDips(audio_path))]
        request.session['df'] = df.to_json()
        request.session.save()
    else:
        json_string = request.session['df']
        df = pd.read_json(json_string)

    context = {'speaking_percentage': str(speakingPercentage(df)), 'rate_of_speech': str(df.loc['rate_of_speech'][0]),
               'articulation_rate': str(df.loc['articulation_rate'][0]), 'gender': str(df.loc['gender'][0]),
               'intonation': str(df.loc['intonation'][0]), 'number_of_pauses': str(df.loc['number_of_pauses'][0]),
               'number_of_syllables': str(df.loc['number_of_syllables'][0]), 'spikes': str(df.loc['Spikes'][0]),
               'dips': str(df.loc['Dips'][0])}
    return render(request, 'main-summary.html', context)

def content(request):
    json_string = request.session['df']
    df = pd.read_json(json_string)
    context={'transcript': str((df.loc['Transcript'][0])), 'average_word_length': str(df.loc['Average Word Length'][0]),
             'average_sentence_length': str(df.loc['Average Sentence Length'][0]), 'lexical_diversity_score': str(df.loc['Lexical Diversity Score'][0]),
             'frequent_words': str(df.loc['Frequent Words'][0]), 'sentiment': str(df.loc['Sentiment'][0]), 'total_words': str(df.loc['Total Words'][0]), 'overall_score': str(df.loc['Overall Score'][0])}
    return render(request, 'content.html', context)

def download_csv(request):
    json_string = request.session['df']
    df = pd.read_json(json_string)
    print(df)
    csv_data = df.to_csv(index=True, encoding='utf-8-sig')

    response = HttpResponse(csv_data, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="voicebox_summary.csv"'

    return response