import numpy as np

class MIX:
    def __init__(self):
        self.inputs = [] 

    def add(self, signal, gain=1.0, pan=0.5):
        self.inputs.append((signal, gain, pan))

    def render(self, frames):
        mix = np.zeros((frames, 2), dtype=np.float32)

        for signal, gain, pan in self.inputs:
            signal = signal[:frames] * gain

            left = signal * np.cos(pan * np.pi / 2)
            right = signal * np.sin(pan * np.pi / 2)

            stereo = np.stack([left, right], axis=1)
            mix += stereo

        self.inputs = []
        return mix
