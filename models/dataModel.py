from libs.filters import *
from libs.signals import *
from scipy import signal

class DataModel():
    def __init__(self):

        self.F = Filter()
        self.H = signal.TransferFunction([1], [1])
        self.filters = []

        self.on_filter_close = lambda: print("DataModel.on_filter_close()")

        self.signal_list = [
            Pulse(),
            Sinewave(),
            RectangularWave(),
            TriangularWave(),
            SawtoothWave(),
            SenoidWithNoise(),
        ]

        self.signal = self.signal_list[0]

        self.linear_scale = False

        # Create signal options
        self.signalOptions = []
        for s in self.signal_list:
            self.signalOptions.append({
                'name': s.name,
                'callback': lambda s=s: setattr(self, 'signal', s),
            })

        # Create filter options
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
            {
                'name': 'Custom Filter',
                'callback': lambda: self.filters.append(CustomFilter(self.on_filter_close)),
            },
            {
                'name': 'High Order Low Pass',
                'callback': lambda: self.filters.append(HighOrderLowPass()),
            },
            {
                'name': 'Second Ord Pole',
                'callback': lambda: self.filters.append(SecondOrdPole()), 
            },
            {
                'name': 'Second Ord Zero',
                'callback': lambda: self.filters.append(SecondOrdZero()), 
            }

        ]