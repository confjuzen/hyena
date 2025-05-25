from evdev import InputDevice, list_devices, categorize, ecodes

def control(synth):
    devices = [InputDevice(path) for path in list_devices()]
    gamepad = None
    for device in devices:
        if "Xbox" in device.name or "Wireless Controller" in device.name:
            gamepad = device
            break
    if gamepad is None:
        print("Xbox controller not found!")
        return

    print(f"Using controller: {gamepad.name}")

    l_stick = 1.0

    for event in gamepad.read_loop():
        if event.type == ecodes.EV_ABS:
            if event.code == ecodes.ABS_X:  # X axis controls LFO speed
                raw_value = event.value  # likely in range -32768 to +32767
                # Normalize to 0..1
                norm = (raw_value + 32768) / 65535
                # Map to LFO freq range, e.g. 0.1Hz to 10Hz
                new_freq = (0.1 + norm * (10 - 0.1)) - 9.0
                l_stick = new_freq
                #print("l_sticl : ", l_stick)
              #  print(f"LFO freq set to {new_freq:.2f} Hz")
                return l_stick   
            #elif event.code == ecodes.ABS_Y:  # Y axis controls LFO amplitude
             #   raw_value = event.value
              #  norm = (raw_value + 32768) / 65535
                # Map to amplitude range, e.g. 0 to 5
               # new_amp = norm * 5
              #  synth.lfo.amplitude = new_amp
                #print(f"LFO amplitude set to {new_amp:.2f}")



