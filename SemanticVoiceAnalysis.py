import os.path
import pickle
import myprosody as sp
# TODO: upload files to audio files directory
p="VoiceAudioTest"
c=r"C:\Users\nagendra_951532\PycharmProjects\VoiceBox\myprosody"
def countPauses(file):
    title = os.path.basename(file)
    print(sp.mysppaus(title,c))

if __name__ == "__main__":
    countPauses(r"C:\Users\nagendra_951532\PycharmProjects\VoiceBox\myprosody\dataset\audioFiles\VoiceAudioTest")
