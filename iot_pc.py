import numpy as np
import matplotlib.pyplot as plt
import librosa
from time import sleep
import playsound
import threading
import socket

socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP宣告

def playMusic(filename: str):
    playsound.playsound(filename)

def play(filename: str):
    """
        播放音樂檔案，使用threading
    """
    t = threading.Thread(target=playMusic, args=(filename, ))
    t.start()

def printLed(val: list):
    """
        將LED訊號以方塊文字來模擬在MAX7219上的樣子
        
        example:
        
        ■ □ □ □ □ □ ■ □
        ■ □ ■ □ □ □ ■ □
        ■ ■ ■ ■ ■ ■ ■ □
        ■ ■ ■ ■ ■ ■ ■ □
        ■ ■ ■ ■ ■ ■ ■ □
        ■ ■ ■ ■ ■ ■ ■ □
        ■ ■ ■ ■ ■ ■ ■ □
        ■ ■ ■ ■ ■ ■ ■ ■

    """
    content = ""
    for i in range(len(val), 0, -1):
        for k in range(len(val)):
            if val[k] >= i: content += '■ '
            else: content += '□ '
        content += '\n'
    
    return content

def main():
    fftsize = 4096
    binedges = [8, 16, 32, 64, 128, 256, 512, 1024, 2048]
    nbins = len(binedges)-1
    offsets = [4, 4, 4, 4, 6, 8, 10, 12]
    nleds = 8
    ledsPerDoubling = 1.0
    binval = 0.001 * np.ones(nbins, np.float)
    newbinval = np.zeros(nbins, np.float)
    decayConst = 0.9

    filename = './music.mp3'

    # 載入音檔
    y, sr = librosa.load(filename, sr=None)
    music = []
    # 將每秒的聲音拆成10份(若音檔為10秒，len(music) = 100)
    for i in range(0, len(y), int(sr/10)):
            music.append(list(y)[i:i+sr])

    ledval = []

    # 建立socket連線
    socket2.connect(("172.20.10.11",9487))
    socket2.send("open".encode())

    play(filename)

    for m in music:
        # 每100ms的音檔
        waveform = m
        # 利用Fast Fourier Transform處理音樂訊號，再轉換成1~8的LED訊號
        spectrum = np.abs(np.fft.rfft(waveform[:fftsize]))
        for i in range(nbins-1):
            newbinval[i] = np.mean(spectrum[binedges[i]:binedges[i+1]])
        binval = np.maximum(newbinval, decayConst*binval)
        ledval = np.round(np.maximum(0, np.minimum(nleds, 
                                                    ledsPerDoubling * np.log2(binval) 
                                                    + offsets)))
        print(ledval) # ex: [4. 3. 2. 2. 1. 3. 5. 0.]
        # 將LED訊號透過socket傳送
        socket2.send(str(ledval).encode())
        sleep(0.1)

    socket2.send("close".encode())

if __name__ == '__main__':
    main()