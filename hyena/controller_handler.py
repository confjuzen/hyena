import pygame

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

def poll_controller(joystick, synth_state):
    pygame.event.pump()

    left = joystick.get_button(15)
    right = joystick.get_button(16)
    up = joystick.get_button(13)
    down = joystick.get_button(14)
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            if left:
                synth_state.switch_module(-1)
            elif right:
                synth_state.switch_module(+1)
            if up:
                synth_state.switch_track(-1)
            elif down:
                synth_state.switch_track(+1)

    buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]
    axes = [joystick.get_axis(i) for i in range(joystick.get_numaxes())]
    return buttons, axes

