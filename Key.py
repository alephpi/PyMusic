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
    pentatonic = [2,2,3,2,3]
    heptatonic = [2,2,1,2,2,2,1]
    # 调式
    MODE = {'hepta_scale':{
                'Ionian': 0,
                'Dorian': 1,
                'Phrygian':2,
                'Lydian':3,
                'Mixolydian':4,
                'Aeolian':5,
                'Locrian':6
                }
            }
    def __init__(self, tonic: Note, mode: str, temperament: Temperament) -> None:
        self.tonic: Note = tonic # define the tonic
        self.scale: OrderedDict[str, float] = {}
        self.temperment = temperament
        if mode in Key.MODE['hepta_scale'].keys():
            rotation = Key.MODE['hepta_scale'][mode]
            aux = deque(Key.heptatonic)
            aux.rotate(rotation)
            indices = [0] + list(accumulate(list(aux)))
            start_index = Key.NOTE_NAME.index(self.tonic.name)
            for i in indices:
                if (i!=12):
                    self.scale[Key.NOTE_NAME[(i + start_index) % len(Key.NOTE_NAME)]] = self.tonic.pitch * self.temperment.ratios[i]  
                else:
                    self.scale[self.tonic.name+'\''] = self.tonic.pitch * self.temperment.ratios[i]
    def __str__(self) -> str:
        return self.scale.__str__()            

# C = Note('C', 256)
# JI = Temperament.JustIntonation()
# C_major = Key(C, 'Ionian', JI)
