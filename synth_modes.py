import pygame

VCO = "VCO"
LFO = "LFO"
ENV = "ENV"

modes = [VCO, LFO, ENV]
mode_index = 0

def synth_mode():
    global mode_index
    mode_text = modes[mode_index]
    return mode_text


def set_synth_mode(direction):
    global mode_index

    if direction == "left":
        mode_index = (mode_index + 1) % len(modes)
    elif direction == "right":
        mode_index = (mode_index - 1) % len(modes)

    mode_text = modes[mode_index]
