class Module:
    def __init__(self, name):
        self.name = name

class Track:
    def __init__(self, name, modules):
        self.name = name
        self.modules = modules
        self.module_index = 0

    @property
    def current_module(self):
        return self.modules[self.module_index]

    def switch_module(self, direction):
        self.module_index = (self.module_index + direction) % len(self.modules)

class SynthState:
    _instance = None

    def __init__(self):
        self.tracks = [
            Track("Synth", [Module("VCO"), Module("LFO")]),
            Track("Synth 2", [Module("VCO"), Module("LFO")]),
            Track("Drum Machine", [Module("Kick"), Module("Snare")])
        ]
        self.track_index = 0

    @classmethod
    def init(cls):
        if cls._instance is None:
            cls._instance = SynthState()

    @classmethod
    def get(cls):
        return cls._instance

    def switch_module(self, direction):
        current_track = self.tracks[self.track_index]
        current_track.switch_module(direction)
        print(f"Switched to module: {current_track.current_module.name}")

    def switch_track(self, direction):
        self.track_index = (self.track_index + direction) % len(self.tracks)
        print(f"Switched to track: {self.tracks[self.track_index].name}")

    def get_module_state(self):
        return f"{self.tracks[self.track_index].current_module.name}"

    def get_track_state(self):
        return f"TRACK {self.track_index + 1}"
