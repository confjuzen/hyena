import pygame
from synth_modes import set_synth_mode

def init_controller():
    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print("No joystick detected")
        exit()

    joystick = pygame.joystick.Joystick(1)
    joystick.init()

    print(f"Joystick name: {joystick.get_name()}")
    return joystick

def poll_controller(joystick):
    pygame.event.pump()

    buttons = [ joystick.get_button(i) for i in range(joystick.get_numbuttons())]
    axes = [ joystick.get_axis(i) for i in range(joystick.get_numaxes()) ]
    
    left = joystick.get_button(15)
    if left == 1:
        set_synth_mode("left")
    right = joystick.get_button(16)
    if right == 1:
        set_synth_mode("right")

    return buttons, axes    


