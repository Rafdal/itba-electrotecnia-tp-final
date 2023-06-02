from backend.filters import *
from scipy import signal

class DataModel():
    def __init__(self):

        self.H = signal.TransferFunction([1], [1])
        self.filters = []
        self.signals = []

        self.filterOptions = [
            {
                'name': 'Gain',
                'callback': lambda: self.filters.append(Gain()),
            },
            {
                'name': 'First Order Low Pass',
                'callback': lambda: self.filters.append(FOLowPass()),
            },
            {
                'name': 'First Order High Pass',
                'callback': lambda: self.filters.append(FOHighPass()),
            },
            {
                'name': 'First Order All Pass',
                'callback': lambda: self.filters.append(FOAllPass()),
            },
            {
                'name': 'Second Order Low Pass',
                'callback': lambda: self.filters.append(SOLowPass()),
            },
            {
                'name': 'Second Order High Pass',
                'callback': lambda: self.filters.append(SOHighPass()),
            },
            {
                'name': 'Second Order All Pass',
                'callback': lambda: self.filters.append(SOAllPass()),
            },
            {
                'name': 'Second Order Band Pass',
                'callback': lambda: self.filters.append(SOBandPass()),
            },
            {
                'name': 'Notch Filter',
                'callback': lambda: self.filters.append(NotchFilter()),
            },
            {
                'name': 'Low Pass Notch',
                'callback': lambda: self.filters.append(LowPassNotch()),
            },
            {
                'name': 'High Pass Notch',
                'callback': lambda: self.filters.append(HighPassNotch()),
            },
        ]