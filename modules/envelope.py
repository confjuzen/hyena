import numpy as np

class ADSR:
    def __init__(self, attack, decay, sustain_level, release, sample_rate):
        self.attack = attack
        self.decay = decay
        self.sustain_level = sustain_level
        self.release = release
        self.sample_rate = sample_rate
        
        self.state = 'idle'   # states: idle, attack, decay, sustain, release
        self.time_in_state = 0
        self.amplitude = 0.0
        
        self.note_on_time = 0
        self.note_off_time = 0
        
    def note_on(self):
        self.state = 'attack'
        self.time_in_state = 0
    
    def note_off(self):
        self.state = 'release'
        self.time_in_state = 0
    
    def process(self, frames):
        envelope = np.zeros(frames)
        for i in range(frames):
            if self.state == 'attack':
                attack_samples = int(self.attack * self.sample_rate)
                self.amplitude = (self.time_in_state / attack_samples) if attack_samples > 0 else 1.0
                if self.time_in_state >= attack_samples:
                    self.state = 'decay'
                    self.time_in_state = 0
            elif self.state == 'decay':
                decay_samples = int(self.decay * self.sample_rate)
                self.amplitude = 1.0 - (1.0 - self.sustain_level) * (self.time_in_state / decay_samples) if decay_samples > 0 else self.sustain_level
                if self.time_in_state >= decay_samples:
                    self.state = 'sustain'
                    self.amplitude = self.sustain_level
            elif self.state == 'sustain':
                self.amplitude = self.sustain_level
            elif self.state == 'release':
                release_samples = int(self.release * self.sample_rate)
                self.amplitude = self.amplitude * (1 - self.time_in_state / release_samples) if release_samples > 0 else 0
                if self.time_in_state >= release_samples:
                    self.state = 'idle'
                    self.amplitude = 0.0
            elif self.state == 'idle':
                self.amplitude = 0.0
                
            envelope[i] = self.amplitude
            self.time_in_state += 1
        return envelope
