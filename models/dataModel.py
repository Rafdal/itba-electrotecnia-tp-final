from backend.filters import *
from scipy import signal

class DataModel():
    def __init__(self):

        self.H = signal.TransferFunction([1], [1])
