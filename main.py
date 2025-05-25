import os
os.environ['ALSA_NO_WARN'] = '1'

import mido
import fluidsynth
import sounddevice as sd
from modules.oscillator import midi_to_freq
from synth import SYNTH
import numpy as np
import threading
import time
from screen import main
from controler import control

sd.default.device = "pipewire"


SAMPLE_RATE = 44100
active_voices = {}  # note -> SYNTH instance

VOICE_LOCK = threading.Lock()  # to protect active_voices in callback & MIDI thread



class SharedAudioBuffer:
    def __init__(self, max_size=44100):
        self.lock = threading.Lock()
        self.left = np.zeros(max_size, dtype=np.float32)
        self.right = np.zeros(max_size, dtype=np.float32)
        self.max_size = max_size
        self.pos = 0  # write position

    def update(self, left_chunk, right_chunk):
        with self.lock:
            chunk_size = len(left_chunk)
            # Circular buffer write
            end_pos = (self.pos + chunk_size) % self.max_size
            if self.pos + chunk_size <= self.max_size:
                self.left[self.pos:self.pos + chunk_size] = left_chunk
                self.right[self.pos:self.pos + chunk_size] = right_chunk
            else:
                part1_len = self.max_size - self.pos
                self.left[self.pos:] = left_chunk[:part1_len]
                self.left[:end_pos] = left_chunk[part1_len:]
                self.right[self.pos:] = right_chunk[:part1_len]
                self.right[:end_pos] = right_chunk[part1_len:]
            self.pos = end_pos

    def get_buffer(self, length):
        with self.lock:
            if self.pos - length < 0:
                # wrap around
                part1_len = length - self.pos
                left_data = np.concatenate((self.left[self.max_size - part1_len:], self.left[:self.pos]))
                right_data = np.concatenate((self.right[self.max_size - part1_len:], self.right[:self.pos]))
            else:
                left_data = self.left[self.pos - length:self.pos]
                right_data = self.right[self.pos - length:self.pos]
            return left_data.copy(), right_data.copy()

shared_audio_buffer = SharedAudioBuffer()


def audio_callback(outdata, frames, time, status):
    with VOICE_LOCK:
        if not active_voices:
            outdata[:] = np.zeros((frames, 2), dtype=np.float32)
            shared_audio_buffer.update(np.zeros(frames), np.zeros(frames))
            return
        
        buffer = np.zeros((frames, 2), dtype=np.float32)
        to_remove = []
        
        for note, synth in active_voices.items():
            wave = synth.generate(frames)
            buffer += wave
            if not synth.active:
                to_remove.append(note)
        
        # Remove voices that finished playing
        for note in to_remove:
            del active_voices[note]
        
        max_amp = np.max(np.abs(buffer))
        if max_amp > 1.0:
            buffer /= max_amp
        
        shared_audio_buffer.update(buffer[:,0], buffer[:,1])
        
        outdata[:] = buffer

stream = sd.OutputStream(
    samplerate=SAMPLE_RATE, 
    channels=2, 
    callback=audio_callback,
    dtype='float32'
)
stream.start()

def note_on_channel_2(msg):
    note = msg.note
    freq = midi_to_freq(note)
    velocity = msg.velocity
    with VOICE_LOCK:
        if note not in active_voices:
            active_voices[note] = SYNTH(freq, velocity, SAMPLE_RATE)
        else:
            # Retrigger envelope if note already exists
            active_voices[note].adsr.note_on()

def note_off_channel_2(msg):
    note = msg.note
    with VOICE_LOCK:
        synth = active_voices.get(note)
        if synth:
            synth.note_off()  # triggers release phase

fs = fluidsynth.Synth()
fs.start(driver="pulseaudio")
sfid = fs.sfload("/usr/share/soundfonts/FluidR3_GM.sf2")
fs.program_select(0, sfid, 0, 0)

input_name = [p for p in mido.get_input_names() if "Behringer" in p][0]

def midi_loop():
    with mido.open_input(input_name) as inport:
        print("Connected to MIDI input:", input_name)
        try:
            for msg in inport:
                if msg.type == 'note_on' and msg.velocity > 0:
                    print(f"Note ON, channel {msg.channel + 1}, note {msg.note}, velocity {msg.velocity}")
                    if msg.channel == 0:
                        fs.noteon(0, msg.note, msg.velocity)
                    elif msg.channel == 1:
                        note_on_channel_2(msg)
                elif msg.type == 'note_off':
                    print(f"Note OFF, channel {msg.channel + 1}, note {msg.note}")
                    if msg.channel == 0:
                        fs.noteoff(0, msg.note)
                    elif msg.channel == 1:
                        note_off_channel_2(msg)

        except KeyboardInterrupt:
            print(" Bye!")
            fs.delete()
            stream.stop()
            stream.close()


synth = SYNTH(freq=440.0, velocity=100, sample_rate=SAMPLE_RATE)

midi_thread = threading.Thread(target=midi_loop, daemon=True)
midi_thread.start()

control(synth)

main()