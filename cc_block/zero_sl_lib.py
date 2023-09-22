
ableton_id = 4

def add_automap_headers(command: int):
  return [0xF0, 0x00, 0x20, 0x29, 0x03, 0x03, 0x12, 0x00, ableton_id, 0x00, *command, 0xF7]

on_command = add_automap_headers([1, 1])
off_command = add_automap_headers([1, 0])

display_command = 2
set_cursor = 1

def fill_row(row: int, text: str):
  return [display_command, set_cursor, 0, row, ord(char) for char in text]