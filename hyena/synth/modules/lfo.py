#import numpy as np
#import time
#
#class LFO:
#    def __init__(self, rate=2.0, depth=5.0, waveform='sine'):
#        self.rate = rate
#        self.depth = depth
#        self.waveform = waveform
#        self.start_time = time.time()
#
#    def value(self, t):
#        phase = 2 * np.pi * self.rate * t
#        if self.waveform == 'sine':
#            return np.sin(phase) * self.depth
#        elif self.waveform == 'square':
#            return self.depth if np.sin(phase) > 0 else -self.depth
#        elif self.waveform == 'triangle':
#            return 2 * self.depth * (abs(2 * ((t * self.rate) % 1) - 1) - 0.5)
#        elif self.waveform == 'saw':
#            return 2 * self.depth * ((t * self.rate) % 1 - 0.5)
#        else:
#            return 0
#