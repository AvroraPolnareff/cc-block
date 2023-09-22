
ableton_id = 4

def add_automap_headers(command: int):
  return [0xF0, 0x00, 0x20, 0x29, 0x03, 0x03, 0x12, 0x00, ableton_id, 0x00, *command, 0xF7]

on_command = add_automap_headers([1, 1])
off_command = add_automap_headers([1, 0])

display_command = 2
set_cursor = 1

left_markers = [81,83,84,80,82]

left_button_rows = range(24, 40, 1)
right_button_rows = range(40, 56, 1)
right_menu_buttons = range(72, 78, 1)

encoder_lights = range(112, 120, 1)

next_page = 88
prev_page = 89

toggle_transport = 79

def fill_row(row: int, text: str):
  return [display_command, set_cursor, 0, row, ord(char) for char in text]

class LauchkeyLights:
    lights = [96, 97, 98, 99, 100, 101, 102, 103, 104, 112, 
              113, 114, 115, 116, 117, 118, 119, 120]
    port = 0x90

    def __init__(self, midiout) -> None:
        self.midiout = midiout

    def init(self):
        self.midiout.send_message([self.port, 0x0C, 0x7F])

    def change_light(self, number, toggle):
        self.midiout.send_message(self.port, self.lights(number), 127 if toggle else 0)
    
    
        