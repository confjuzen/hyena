# Create VCO and ADSR per note
from modules.oscillator import VCO
from modules.envelope import ADSR

class SYNTH:
    def __init__(self, freq, velocity, sample_rate):
        self.vco = VCO(freq, velocity / 127.0, sample_rate)
        self.adsr = ADSR(attack=0.3, decay=3.0, sustain_level=5.0, release=5.0, sample_rate=sample_rate)
        self.adsr.note_on()
        self.active = True
    
    def note_off(self):
        self.adsr.note_off()
    
    def generate(self, frames):
        wave = self.vco.generate(frames)
        envelope = self.adsr.process(frames)
        output = wave * envelope
        # Mark inactive if envelope finished
        if self.adsr.state == 'idle':
            self.active = False
        return output
