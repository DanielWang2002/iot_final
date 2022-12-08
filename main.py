import numpy as np
import matplotlib.pyplot as plt
import librosa
from time import sleep
import playsound
import threading

def playMusic(filename: str):
    playsound.playsound(filename)

def play(filename: str):
    t = threading.Thread(target=playMusic, args=(filename, ))
    t.start()

def printLed(val: list):
    content = ""
    for i in range(len(val), 0, -1):
        for k in range(len(val)):
            if val[k] >= i: content += '■ '
            else: content += '□ '
        content += '\n'
    
    return content

def main():
    fftsize = 4096  # about 100ms at 44 kHz; each bin will be ~ 10 Hz
    # Band edges to define 8 octave-wide ranges in the FFT output
    binedges = [8, 16, 32, 64, 128, 256, 512, 1024, 2048]
    nbins = len(binedges)-1
    # offsets to get our 48 dB range onto something useful, per band
    offsets = [4, 4, 4, 4, 6, 8, 10, 12]
    # largest value in ledval
    nleds = 8
    # scaling of LEDs per doubling in amplitude
    ledsPerDoubling = 1.0
    # initial value of per-band energy history
    binval = 0.001 * np.ones(nbins, np.float)
    newbinval = np.zeros(nbins, np.float)
    # How rapidly the displays decay after a peak (depends on how often we're called)
    decayConst = 0.9

    # somehow tap into the most recent 30-100ms of audio.  
    # Assume we get 44 kHz mono back
    filename = './music.mp3'
    y, sr = librosa.load(filename, sr=None)
    music = []
    for i in range(0, len(y), int(sr/10)):
            music.append(list(y)[i:i+sr])

    ledval = []

    play(filename)

    for m in music:
        waveform = m
        # find spectrum
        spectrum = np.abs(np.fft.rfft(waveform[:fftsize]))

        # gather into octave bands    
        for i in range(nbins-1):
            newbinval[i] = np.mean(spectrum[binedges[i]:binedges[i+1]])
        # Peak smoothing - decay slowly after large values
        binval = np.maximum(newbinval, decayConst*binval)
        # Quantize into values 0..8 as the number of leds to light in each column
        ledval = np.round(np.maximum(0, np.minimum(nleds, 
                                                    ledsPerDoubling * np.log2(binval) 
                                                    + offsets)))
        print(printLed(ledval))
        sleep(0.1)
        # print(ledval)
        # Now illuminate ledval[i] LEDs in column i (0..7) ...

if __name__ == '__main__':
    main()