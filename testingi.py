from pydub import AudioSegment
import math
import time
import pandas as pd

audio = AudioSegment.from_file("VoiceAudioTest.wav")
time_split = 1 * 1000
length = len(audio)
volume_list=[]

for i in range(math.floor(length/time_split)):
    start = time_split * i
    end = time_split * (i+1)
    if end >= length:
        end = length
    loudness_audio = audio[start:end].dBFS
    print("-"*(math.ceil(abs(loudness_audio)))+str(start)+"-"+str(end)+": "+str(loudness_audio)+" dBFS")
    volume_list.append(loudness_audio)
    #time.sleep(1)

df = pd.DataFrame(volume_list)
print(df.head())