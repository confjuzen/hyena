import numpy as np

def midi_to_freq(midi_note):
    return 440.0 * (2.0 ** ((midi_note - 69) / 12.0))

class VCO:
    def __init__(self, freq, amplitude, sample_rate):
        self.freq = freq
        self.amplitude = amplitude
        self.sample_rate = sample_rate
        self.phase = 0.0

    def generate(self, frames):
        t = (np.arange(frames) + self.phase) / self.sample_rate
        wave = self.amplitude * np.sin(2 * np.pi * self.freq * t)
        self.phase = (self.phase + frames) % self.sample_rate
        return wave
