import librosa
import librosa.display
import matplotlib.pyplot as plt
import threading
import playsound
import numpy as np
import pandas as pd
from time import sleep
from typing import Tuple
from pprint import pprint
import random as r

def playMusic(filename: str):
    playsound.playsound(filename)

def play(filename: str):
    t = threading.Thread(target=playMusic, args=(filename, ))
    t.start()

def sliceInteger(num: int) -> list:
    # 將整數切成八份
    d = num / 8
    ret = []
    #16 =  [16, 14, 12, 10, 8, 6, 4, 2]
    for i in range(0, 8):
        ret.append(num - (d*i))
    return ret

def divideInteger(num: int) -> list:
    ret = [num]
    for i in range(7):
        ret.append(int(num/2))
        num = int(num/2)
    return ret

def piff(val):
    return int(2*4096*val/22050)

def getMusicMeanPerSecond(music: list, sr: int) -> Tuple[list, list]:
    """
        return (每秒的音頻高低切成八等份後，每份的平均) 以及 (每秒的音量全距切成八等份)
    """

    totalMean = [] # 每秒的八份平均音量
    rangeMean = [] # 每秒的音量全距切成八等份
    for i in music:
        distance = sliceInteger(max(i) - min(i))
        # print(distance)
        sr_slice = sliceInteger(sr)
        secMean = [0.0] * 8
        for k in range(0, 8):
            # if (k != 7): secMean[k] = np.mean(i[int(sr_slice[k+1]) : int(sr_slice[k])])
            if (k != 7): secMean[k] = max(i[int(sr_slice[k+1]) : int(sr_slice[k])]) - min(i[int(sr_slice[k+1]) : int(sr_slice[k])])
            else: secMean[k] = max(i[int(sr_slice[k]) : int(sr_slice[k-1])])
        # print(secMean)
        totalMean.append(secMean)
        rangeMean.append(distance)
    return totalMean, rangeMean

def getSignalOfMusic(perSecMean: list, rangeMean: list) -> list:
    """
        判斷每秒的八個分段中，每個分段的平均分貝屬於全距中的哪個位置(以0~7標示)
    """

    signal = [[0]*len(perSecMean[0]) for i in range(len(perSecMean))]
    
    # 每秒的資料
    for i in range(0, len(perSecMean)):
        # 每秒資料分成八段
        for k in range(0, len(perSecMean[i])):
            # 全距分成八段
            rangeMean[i].reverse()
            for j in range(0, len(rangeMean[i])):
                print(i, k, j, perSecMean[i][k], rangeMean[i][j], perSecMean[i][k] <= rangeMean[i][j])
                if perSecMean[i][k] <= rangeMean[i][j]:
                    signal[i][k] = j
                    break

    
                        
    
    return signal

def main():
    filename = './music.mp3'
    y, sr = librosa.load(filename, sr=None)
    print(sr)
    music = []

    for i in range(0, len(y), sr):
        music.append(list(y)[i:i+sr])
    
    perSecMean, rangeMean = getMusicMeanPerSecond(music, sr)

    pprint(perSecMean)
    # librosa.display.waveshow(np.array(music[0]), sr=sr)
    # plt.show()
    # print(max(music[0]))
    # print(max(music[0][0:2756]))
    # print(perSecMean[0], perSecMean[1])


    # for i, k in enumerate(music):
    #     plt.plot([j for j in range(0, 22050)], k)
    #     plt.show()
    #     if i == 1: break
    
    # for i in range(0, 10):
    #     for k in range(0, 8):
    #         for j in range(0, 10):
    #             for v in range(0, 8):
    #                 if perSecMean[i][k] >= rangeMean[j][v]: print(perSecMean[i][k], rangeMean[j][v])
    # signal = getSignalOfMusic(perSecMean, rangeMean)
    # print(signal)
    # print(max(perSecMean[0]))
    


if __name__ == '__main__':
    main()

    

# plt.figure()
# librosa.display.waveshow(y, sr=sr)
# plt.show()
# play(filename)
# print('playing music...')