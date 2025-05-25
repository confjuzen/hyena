import urwid

class WaveformWidget(urwid.Widget):
    def __init__(self, shared_audio_buffer):
        super().__init__()
        self.shared_audio_buffer = shared_audio_buffer

    def selectable(self):
        return False

    def rows(self, size, focus=False):
        # Decide how tall your widget should be, e.g., 20 lines
        return 20

    def render(self, size, focus=False):
        maxcol = size[0]

        # Example: Build rows as list of bytes lines, width should be <= maxcol
        # This is just a placeholder: replace with your actual waveform drawing logic
        waveform_lines = [
            b"".ljust(maxcol, b" "),  # blank line
            b"Waveform".ljust(maxcol, b" "),  # sample text padded to width
            b"".ljust(maxcol, b" ")
        ]

        # Create TextCanvas with maxcol only (no maxrow)
        canvas = urwid.TextCanvas(waveform_lines, maxcol=maxcol)

        return canvas


def run_waveform_ui(shared_audio_buffer):
    # Create your widget with the shared_audio_buffer
    waveform_widget = WaveformWidget(shared_audio_buffer)

    # Use a filler to expand the widget vertically and horizontally
    fill = urwid.Filler(waveform_widget, valign='top')

    # Create the urwid main loop
    loop = urwid.MainLoop(fill)

    # Run the UI loop in the main thread (blocking call)
    loop.run()
