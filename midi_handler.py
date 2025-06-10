import mido

def list_midi_ports():
    return mido.get_input_names()

def open_midi_input(callback):
    for name in mido.get_input_names():
        if "Behringer" in name or "Swing" in name:
            port = mido.open_input(name, callback=callback)
            print(f"Connected to: {name}")
            return port
    print("Behringer Swing not found.")
    return None
