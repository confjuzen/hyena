import pygame
import numpy as np
import audio_engine 


def init_ui():
    pygame.init()
    screen = pygame.display.set_mode((640, 240))
    pygame.display.set_caption("hyena")
    return screen


def draw_waveform(screen, samples=512):
    wave = audio_engine.get_current_waveform(samples)
    width, height = screen.get_size()
    center_y = height // 2
    scale = height / 1.2

    for x in range(samples - 1):
        x1 = int((x / samples) * width)
        x2 = int(((x + 1) / samples) * width)
        y1 = int(center_y - wave[x] * scale)
        y2 = int(center_y - wave[x + 1] * scale)
        pygame.draw.line(screen, (200, 0, 200), (x1, y1), (x2, y2),width=2)

def draw_ui(screen, loop_progress, bpm, synth_text):
    screen.fill((20, 0, 20))
    pygame.draw.rect(screen, (200, 0, 200), (0, 237, int(640 * loop_progress), 3))
    draw_waveform(screen)
    font = pygame.font.Font("./Montserrat.ttf", 18)
    bpm_text = font.render(f"BPM: {bpm:.1f}", True, (200, 0, 200))
    screen.blit(bpm_text, (screen.get_width() - 130, 10))

    pygame.draw.rect(screen, (60, 0, 60),( 20, 10, 85, 28))
    state_text = font.render(synth_text, True, (200, 0, 200))
    screen.blit(state_text, (40, 12))


    pygame.display.flip()