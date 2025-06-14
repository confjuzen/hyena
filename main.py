import time
from collections import deque

import hyena.midi_handler as midi_handler

import hyena.ui as ui
import hyena.synth.audio_engine as audio_engine
import hyena.controller_handler as controller_handler
from hyena.state import SynthState

clock_ticks = 0
last_tick_times = deque(maxlen=24)
tick_times = deque(maxlen=48)
loop_start_time = time.time()
loop_length_beats = 4
bpm = 120.0

active_notes = {}

def midi_callback(msg):
    global clock_ticks, bpm, loop_start_time

    if msg.type == 'clock':
        now = time.time()
        tick_times.append(now)
        if len(tick_times) >= 2:
            elapsed = tick_times[-1] - tick_times[0]
            tps = len(tick_times) / elapsed
            bpm = (tps / 24) * 60
        clock_ticks += 1

    elif msg.type == 'start':
        clock_ticks = 0
        loop_start_time = time.time()
        print("[MIDI] START received — resetting loop")

    elif msg.type == 'stop':
        print("[MIDI] STOP")

    elif msg.type == 'note_on' and msg.velocity > 0:
        freq = 440.0 * 2 ** ((msg.note - 69) / 12)
        active_notes[msg.note] = freq
        audio_engine.note_on(freq)
        print(f"Note ON: {msg.note} -> {freq:.2f} Hz")

    elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
        freq = active_notes.get(msg.note)
        if freq:
            audio_engine.note_off(freq)
            del active_notes[msg.note]
            print(f"Note OFF: {msg.note}")

def main():
    SynthState.init()
    synth_state = SynthState.get()
    screen = ui.init_ui()
    joystick = controller_handler.init_controller()
    midi_port = midi_handler.open_midi_input(midi_callback)
    if not midi_port:
        return
    stream = audio_engine.start_audio()
    while True:
        now = time.time()
        beats = clock_ticks / 24
        loop_progress = (beats % loop_length_beats) / loop_length_beats
        controller_handler.poll_controller(joystick, synth_state)
        ui.draw_ui(screen, loop_progress, bpm, synth_state.get_module_state(), synth_state.get_track_state())

if __name__ == "__main__":
    main()
