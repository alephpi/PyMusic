class Note: 
    

    def __init__(self, char: str, freq: float):
        self.name = char
        self.pitch = freq
    def __str__(self):
        return "%s\t%f" % (self.name, self.pitch)