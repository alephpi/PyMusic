from collections import deque
from itertools import accumulate
from typing import OrderedDict
from Temperament import Temperament
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
        
    def __init__(self, tonic: Note, mode: str, temperament: Temperament) -> None:
        self.tonic: Note = tonic # define the tonic
        self.scale: OrderedDict[str, float] = {}
        self.temperament = temperament
        if mode in Key.MODE['diatonic'].keys():
            rotation = Key.MODE['diatonic'][mode]
            aux = deque(Key.diatonic)
        elif mode in Key.MODE['pentatonic'].keys():
            rotation = Key.MODE['pentatonic'][mode]
            aux = deque(Key.pentatonic)
        aux.rotate(-rotation)
        indices = [0] + list(accumulate(list(aux)))
        start_index = Key.NOTE_NAME.index(self.tonic.name)
        for i in indices:
            if (i!=12):
                self.scale[Key.NOTE_NAME[(i + start_index) % len(Key.NOTE_NAME)]] = round(self.tonic.pitch * self.temperament.ratios[i], Key.digit)  
            else:
                self.scale[self.tonic.name+'\''] = round(self.tonic.pitch * self.temperament.ratios[i], Key.digit)
    def __str__(self) -> str:
        return self.scale.__str__()            

# C = Note('C', 256)
# JI = Temperament.JustIntonation()
# C_major = Key(C, 'Ionian', JI)
