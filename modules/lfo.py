import numpy as np

class LFO:
    def __init__(self, freq, amplitude, sample_rate):
        self.freq = freq
        self.amplitude = amplitude
        self.sample_rate = sample_rate
        self.phase = 0.0

    def generate(self, frames):
        t = (np.arange(frames) + self.phase) / self.sample_rate
        lfo = self.amplitude * np.sin(2 * np.pi * self.freq * t)
        self.phase = (self.phase + frames) % self.sample_rate
        return lfo