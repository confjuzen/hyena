import sounddevice as sd
import numpy as np
import threading

sd.default.device = "pipewire"

fs = 44100
active_notes = set()

amplitude = 0.2

lock = threading.Lock()

def generate_wave(t):
    if not active_notes:
        return np.zeros_like(t)
    wave = sum(amplitude * np.sin(2 * np.pi * freq * t) for freq in active_notes)
    wave /= len(active_notes)
    return wave

def audio_callback(outdata, frames, time, status):
    with lock:
        t = (np.arange(frames) + audio_callback.frame) / fs
        outdata[:] = generate_wave(t).reshape(-1, 1)
        audio_callback.frame += frames

audio_callback.frame = 0

def start_audio():
    stream = sd.OutputStream(
        samplerate=fs,
        channels=1,
        callback=audio_callback,
        blocksize=512,
    )
    stream.start()
    return stream

def note_on(freq):
    with lock:
        active_notes.add(freq)

def note_off(freq):
    with lock:
        active_notes.discard(freq)

def get_current_waveform(samples=512):
    t = np.linspace(0, samples / fs, samples, endpoint=False)
    with lock:
        if not active_notes:
            return np.zeros_like(t)
        wave = sum(amplitude * np.sin(2 * np.pi * freq * t) for freq in active_notes)
        wave /= len(active_notes)
    return wave

