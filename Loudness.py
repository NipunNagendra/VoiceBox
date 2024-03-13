import matplotlib.pyplot as plt
import numpy as np
import wave


def normalize(path: str):
    raw = wave.open(path)

    signal = raw.readframes(-1)
    signal = np.frombuffer(signal, dtype="int16")

    f_rate = raw.getframerate()

    time = np.linspace(
        0,
        len(signal) / f_rate,
        num=len(signal)
    )

    plt.figure(1)

    plt.title("Sound Wave")

    plt.xlabel("Time")
    plt.plot(time, signal)
    loudness_high = np.abs(signal).max()
    loudness_low = np.abs(signal).min()
    avg = ((loudness_high - loudness_low) / 2)
    print(loudness_high, loudness_low, avg)
    plt.axhline(y=avg, color='r', linestyle='-')
    plt.axhline(y=-avg, color='r', linestyle='-')

    return time, signal, avg


def volumeSpikes(path):
    time, signal, avg = normalize(path)
    spikes = []
    mean = np.mean(signal)
    threshold = 0.4
    index = 0
    while (index < len(signal)):
        if ((np.abs(signal[index]) - avg) / avg) >= threshold:
            spikes.append(time[index])
            index += np.where(time >= time[index] + 0.1)[0][0]
        else:
            index += 1
    return spikes


def volumeDips(path):
    time, signal, avg = normalize(path)
    dips = []
    mean = np.mean(signal)
    threshold = 0.4
    index = 0
    while (index < len(signal)):
        if ((np.abs(signal[index]) - avg) / avg) <= -threshold:
            dips.append(time[index])
            index += np.where(time >= time[index] + 0.1)[0][0]
        else:
            index += 1
    return dips
