

class Param():
    def __init__(self, value=0.0, name="", unit="", scale="linear", range=[0.0, 10.0]):
        self.value = value
        self.name = name
        self.unit = unit
        self.scale = scale
        self.min = range[0]
        self.max = range[1]