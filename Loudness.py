import matplotlib.pyplot as plt
import numpy as np
import wave, sys
 
def visualize(path: str):
   
    raw = wave.open(path)

    signal = raw.readframes(-1)
    signal = np.frombuffer(signal, dtype ="int16")
     
    f_rate = raw.getframerate()

    time = np.linspace(
        0, 
        len(signal) / f_rate,
        num = len(signal)
    ) 

    plt.figure(1)
     
    plt.title("Sound Wave")
     
    plt.xlabel("Time")
    plt.plot(time, signal)
    """lowerv=np.where(time>=7.8)[0]
    upperv=np.where(time>=8.1)[0]

    print(lowerv[0])
    print(upperv[0])

    plt.plot(time[lowerv[0]:upperv[0]], signal[lowerv[0]:upperv[0]])"""

    plt.show()
    return time, signal

def volumeSpikes(time, signal):
    spikes=[]
    mean=np.mean(signal)
    threshold=0.8
    index=0
    while(index<len(signal)):
        if ((signal[i]-mean)/mean)>=threshold:
            spikes.append(time[i])
            i+=1
        else:
            index
    return spikes
 
if __name__ == "__main__":
    time, signal = visualize("VoiceAudioTest.wav")
    print(volumeSpikes(time, signal))
    
