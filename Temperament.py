import math
from typing import List
# from collections import OrderedDict
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
   def PythagorasTemperament(cls):
      ratios = [0] * 13
      ratios[0] = 1
      log2_perfect_fifth = math.log2(3/2)
      n = 0
      for i in range(1,Temperament.num):
         n += 7
         ratios[n % 12] = (3 ** i / 2 ** (i + math.floor(i * log2_perfect_fifth)))
      ratios[12] =  2 * (3 ** 12 / 2 ** (12 + math.floor(12 * log2_perfect_fifth)))
      return cls(ratios)

   def __str__(self) -> str:
      return self.intervals.__str__() 