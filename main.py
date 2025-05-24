import os
os.environ['ALSA_NO_WARN'] = '1'

import mido
import fluidsynth
import sounddevice as sd
from modules.oscillator import midi_to_freq
from synth import SYNTH
import numpy as np
import threading

sd.default.device = "pipewire"

SAMPLE_RATE = 44100
active_voices = {}  # note -> SYNTH instance

VOICE_LOCK = threading.Lock()  # to protect active_voices in callback & MIDI thread

def audio_callback(outdata, frames, time, status):
    with VOICE_LOCK:
        if not active_voices:
            outdata[:] = np.zeros((frames, 1), dtype=np.float32)
            return
        
        buffer = np.zeros(frames, dtype=np.float32)
        to_remove = []
        
        for note, synth in active_voices.items():
            wave = synth.generate(frames)
            buffer += wave
            if not synth.active:
                to_remove.append(note)
        
        # Remove voices that finished playing
        for note in to_remove:
            del active_voices[note]
        
        # Prevent clipping: normalize if necessary
        max_amp = np.max(np.abs(buffer))
        if max_amp > 1.0:
            buffer /= max_amp
        
        outdata[:] = buffer.reshape(-1, 1)

stream = sd.OutputStream(
    samplerate=SAMPLE_RATE, 
    channels=1, 
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
