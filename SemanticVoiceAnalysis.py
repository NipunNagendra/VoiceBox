import os.path
import pickle

import pandas as pd

import myprosody as mysp

# TODO: upload files to audio files directory

# df example:                            0
# number_of_syllables      898
# number_of_pauses         139
# rate_of_speech             3
# articulation_rate          4
# speaking_duration      208.1
# original_duration      329.3
# balance                  0.6
# f0_mean                131.1
# f0_std                  33.7
# f0_median              123.6
# f0_min                    72
# f0_max                   411
# f0_quantile25            107
# f0_quan75                147
# gender                  Male
# intonation           Reading

def voiceAnalysis(file):
    #TODO: change the path to the audio file
    c = r"/Users/nipun/PycharmProjects/VoiceBox/webapp/media/myprosody"
    p = os.path.basename(file)
    df = mysp.mysptotal(p, c)
    x=mysp.myspgend(p, c)
    df.loc['gender'] = x[0].split(",")[0][2:]
    df.loc['intonation'] = x[0].split(",")[1][17:]
    df=df.rename(index={'number_ of_syllables': 'number_of_syllables'})
    return df
def speakingPercentage(df):
    return int((float(df.loc['speaking_duration'])/float(df.loc['original_duration']))*100)




if __name__ == "__main__":
    print(voiceAnalysis(r"/speech_audio"))
