from turtle import left
# class ratio: 
#     def __init__(self, left, right):
#         self.left = left
#         self.right = right
class Interval:
    def __init__(self, name: str, ratio: float):
        self.name = name
        self.ratio = ratio 
    def __repr__(self):
        return "%s\t%.4f" % (self.name, self.ratio)
