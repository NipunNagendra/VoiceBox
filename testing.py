from pydub import AudioSegment


video = AudioSegment.from_file("C:\\Users\\nagendra_951532\\Documents\\VoiceBox\\VoiceAudioTest.mp3", format="mp3")
time_split = 1 * 1000
length = len(video)

for i in range(length):
    time = time_split
    print(video.dbfs(time))
    time+=time_split