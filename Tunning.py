"""This file contains code used in "PyMusic",
by MAO Sicheng, available from https://github.com/alephpi/PyMusic/

Copyright 2022 MAO Sicheng
License: MIT License (https://opensource.org/licenses/MIT)
"""

from collections import deque, OrderedDict
from itertools import accumulate
from typing import List,OrderedDict
import numpy as np
import math
import matplotlib.pyplot as plt
from functools import reduce
import warnings
try:
    from thinkdsp import CosSignal, Wave
except:
    warnings.warn(
        "Can't import thinkdsp;" "Please install the module from https://github.com/AllenDowney/ThinkDSP/blob/master/code/thinkdsp.py"
    )

class Interval:
    def __init__(self, name: str, ratio: float):
        self.name = name
        self.ratio = ratio 
    def __repr__(self):
        return "%s\t%.4f" % (self.name, self.ratio)

class Temperament:
   num = 12 #number of tones
   MUSIC_INTERVAL_NAME = ['unison',
                    'minor second',
                    'major second',
                    'minor third',
                    'major third',
                    'perfect fourth',
                    'tritone',
                    'perfect fifth',
                    'minor sixth',
                    'major sixth',
                    'minor seventh',
                    'major seventh',
                    'octave']
   
   def __init__(self, ratios: List[float]) -> None:
      self.ratios: List[float] = ratios #record the intervals for a certain temperament
      self.intervals: List[Interval] = []
      for i in range(Temperament.num+1):
         self.intervals.append(Interval(Temperament.MUSIC_INTERVAL_NAME[i], self.ratios[i])) #precise frequency ratio per interval

   @classmethod
   def JustIntonation(cls):
      just_ratios = [1, 16/15, 9/8, 6/5, 5/4, 4/3, 45/32, 3/2, 8/5, 5/3, 9/5, 15/8, 2] #tone/root
      return cls(just_ratios)

   @classmethod
   def SanfenSunyifa(cls): #每步或损或益，但均保持管长比介于二分之一与一之间。
      Huangzhong = 81
      QingHuangzhong = Huangzhong/2
      yin = Huangzhong
      GuanChang = [Huangzhong]
      num = 0
      while(num < Temperament.num):
         sun = yin * 2/3
         yi  = yin * 4/3
         if sun < QingHuangzhong:
            yin = yi
         elif yi > Huangzhong:
            yin = sun
         else: #only happens when yin = 3/4
            pass #no else in execution for yin never equal to 3/4
         num += 1
         GuanChang.append(yin)
      GuanChang[-1] /= 2 #最后一个须是清黄钟，手动调整
      ratios = [81/GuanChang[i] for i in range(len(GuanChang))]
      ratios.sort()
      print(GuanChang)
      return cls(ratios)

   @classmethod
   def PythagorasTemperament(cls): #each time raise a perfect fifth, always keeping the frequency ratio inside [1,2]
      ratios = [0] * 13
      ratios[0] = 1
      log2_perfect_fifth = math.log2(3/2)
      n = 0
      for i in range(1,Temperament.num):
         n += 7
         ratios[n % 12] = (3 ** i / 2 ** (i + math.floor(i * log2_perfect_fifth)))
      ratios[12] =  2 * (3 ** 12 / 2 ** (12 + math.floor(12 * log2_perfect_fifth)))
      return cls(ratios)
   
   #SanfenSunyifa is essentially similar to the pythagoras temperament but with different points of view

   @classmethod
   def EqualTemperament(cls):
      ratio = 2 ** (1/Temperament.num) # 朱载堉
      ratios = [ratio ** i for i in range(Temperament.num+1)]
      return cls(ratios)

   def __str__(self) -> str:
      return self.intervals.__str__() 


class Note: 
    def __init__(self, char: str, freq: float):
        self.name = char
        self.pitch = freq
    def __str__(self):
        return "%s\t%f" % (self.name, self.pitch)


class Key:
    NOTE_NAME = ['A','A#','B','C','C#','D','D#','E','F','F#','G','G#']
    #对于十二律而言，五声音阶一共能产生C(12,5)*5=3960种调式
    pentatonic = [2,2,3,2,3] #民族五声音阶
    #对于十二律而言，七声音阶一共能产生C(12,7)*7=5544种调式
    diatonic = [2,2,1,2,2,2,1] #自然七声音阶
    harmonic_minor = [2,1,2,2,1,3,1]
    harmonic_major = [2,2,1,2,1,3,1]
    melodic_minor = [2,1,2,2,2,2,1]
    digit = 4 #display
    # 调式
    MODE = {'diatonic':{
                'Ionian': 0,
                'Dorian': 1,
                'Phrygian':2,
                'Lydian':3,
                'Mixolydian':4,
                'Aeolian':5,
                'Locrian':6
                },
            'pentatonic':{
                'Gong': 0,
                'Shang':1,
                'Jue':2,
                'Zhi':3,
                'Yu':4
                }   
            }
        
    def __init__(self, tonic: Note, scale: list, rotation: int, temperament: Temperament) -> None:
        self.tonic: Note = tonic # define the tonic
        note_rotation = Key.NOTE_NAME.index(self.tonic.name)
        aux = deque(Key.NOTE_NAME)
        aux.rotate(-note_rotation)
        self.notes: list = list(aux)
        self.tonality: OrderedDict[str, float] = {}
        self.temperament = temperament
        aux = deque(scale)
        aux.rotate(-rotation)
        self.indices = [0] + list(accumulate(list(aux)))
        # start_index = Key.NOTE_NAME.index(self.tonic.name)
        for i in self.indices:
            if (i!=12):
                self.tonality[self.notes[i]] = round(self.tonic.pitch * self.temperament.ratios[i], Key.digit)  
            else:
                self.tonality[self.tonic.name+'\''] = round(self.tonic.pitch * self.temperament.ratios[i], Key.digit)
    @classmethod
    def from_classical_mode(cls, tonic:Note, mode: str, temperament: Temperament):
        if mode in Key.MODE['diatonic'].keys():
            rotation = Key.MODE['diatonic'][mode]
            scale = Key.diatonic
        elif mode in Key.MODE['pentatonic'].keys():
            rotation = Key.MODE['pentatonic'][mode]
            scale = Key.pentatonic
        return cls(tonic, scale, rotation, temperament)

    def __str__(self) -> str:
        return self.scale.__str__()            

    def plot(self, mode=None):
        
        labels = self.notes
        ratios = self.temperament.ratios
        log_ratios = np.log2(ratios)
        xval = np.sin(2*np.pi*log_ratios)
        yval = np.cos(2*np.pi*log_ratios)
        fig = plt.figure(1,figsize = [5,5])
        ax = fig.add_subplot(111)

        ax.set_xlim([-1.5,1.5])
        ax.set_ylim([-1.5,1.5])
        ax.axis('off')
        draw_circle = plt.Circle((0,0),1, fill = False)
        #plot points
        ax.plot(xval,yval,'o')
        #plot labels
        for i in range(len(labels)):
            ax.text(1.2*xval[i],1.2*yval[i],labels[i])
        ax.text(1.2*xval[-1],1.2*yval[-1], self.tonic.name+'\'') #add the octave of tonic
        #plot polygon or rayon
        xnode = [xval[i] for i in self.indices]
        ynode = [yval[i] for i in self.indices]
        if mode in  ['p','polygon']:
            for i in range(len(self.indices)):
                ax.plot(xnode[i:i+2],ynode[i:i+2],'r-')
        if mode in  ['r','rayon']:
            for i in self.indices:
                ax.plot([0,xval[i]],[0,yval[i]],'c-')
        ax.set_aspect(1)
        ax.add_artist(draw_circle)

    def make_audio(self, timbre = 'pure', duration= 1, framerate=44100 ):
        freqs = [i for i in self.tonality.values()]
        signals = [CosSignal(freq=freq) for freq in freqs]
        waves = [signal.make_wave(duration=duration, framerate=framerate) for signal in signals]
        wave = reduce(Wave.__or__,waves)
        wave.apodize()
        return wave.make_audio()
        
# test scripts
# C = Note('C', 256)
# D = Note('D', 288)
# JI = Temperament.JustIntonation()
# S = Temperament.SanfenSunyifa()

# C_major = Key(C, 'Ionian', JI)
# D_major = Key(D, 'Ionian', JI)
# Dorian_C = Key(C, 'Dorian', JI)
# Dorian_D = Key(D, 'Dorian', JI)


# Gong_C = Key(C, 'Gong', S)
# Gong_D = Key(D, 'Gong', S)
# Shang_C = Key(C, 'Shang', S)
# Shang_D = Key(D, 'Shang', S)

