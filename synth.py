from modules.oscillator import VCO
from modules.envelope import ADSR
from modules.lfo import LFO
from modules.mix import MIX
from controler import control

import numpy as np

class SYNTH:

    def __init__(self, freq, velocity, sample_rate):

        #l_stick = 1

        self.vco = VCO(freq, velocity / 127.0, sample_rate)
        
        self.vco_octave = VCO(freq * 4.0, velocity / 127.0, sample_rate)

        self.adsr = ADSR(attack=0.01, decay=3.0, sustain_level=2.0, release=5.0, sample_rate=sample_rate)
        self.adsr.note_on()
        self.lfo = LFO(freq= 1.0, amplitude=4.0, sample_rate=sample_rate)

        self.active = True


    def note_off(self):
        self.adsr.note_off()
    
    def generate(self, frames):
        wave = self.vco.generate(frames)
        wave_octave = self.vco_octave.generate(frames)

        envelope = self.adsr.process(frames)
        lfo = self.lfo.generate(frames)

        left = wave * envelope *  (lfo - 1)
        right = wave_octave * envelope *  ( lfo - 1)

        #print("l_stick synth : ", l_stick )

        mixed = (wave + wave_octave) / 2 * envelope   * lfo

        if self.adsr.state == 'idle':
            self.active = False

        mix = MIX()
                #left = pan 0   -   right = pan 1
        mix.add(left, gain=1.0, pan=0.3)
        mix.add(right, gain=1.0, pan=0.7)

        return mix.render(frames)

