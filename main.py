import time
import midi_handler
import audio_engine
import ui
from synth_modes import synth_mode

import controller_handler

from collections import deque

clock_ticks = 0
last_tick_times = deque(maxlen=24)
loop_start_time = time.time()
loop_length_beats = 4
tick_times = deque(maxlen=48)
bpm = 120.0
def update_bpm_from_clock():
    global bpm
    now = time.time()  # seconds
    tick_times.append(now)
    if len(tick_times) >= 2:
        elapsed = tick_times[-1] - tick_times[0]
        num_ticks = len(tick_times)
        tps = num_ticks / elapsed
        bps = tps / 24
        bpm = bps * 60
    return bpm

active_notes = {}

def midi_callback(msg):
    global clock_ticks, bpm, loop_start_time

    if msg.type == 'clock':
        bpm = update_bpm_from_clock()
        clock_ticks += 1

    elif msg.type == 'start':
        clock_ticks = 0
        loop_start_time = time.time()
        print("[midi] START received — resetting loop")

    elif msg.type == 'stop':
        print("[midi] STOP")

    if msg.type == 'style':
        print("scale :", msg.style)

    if msg.type == 'note_on' and msg.velocity > 0:
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
    screen = ui.init_ui()
    midi_port = midi_handler.open_midi_input(midi_callback)
    controller = controller_handler.init_controller()
    audio_engine.start_audio()
    start_time = time.time()
    synth_text = synth_mode()
    while True:
        now = time.time()
        beats = clock_ticks / 24
        loop_progress = (beats % loop_length_beats) / loop_length_beats
        ui.draw_ui(screen, loop_progress, bpm, synth_text)
        axes, buttons = controller_handler.poll_controller(controller)

        time.sleep(0.016)

if __name__ == "__main__":
    main()
