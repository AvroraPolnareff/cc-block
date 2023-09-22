import time
import rtmidi

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
        


class Sequencer:
    isPlay = False
    position = 0
    data = []

    def __init__(self, size = 16) -> None:
        self.data = [0] * size
        self.size = size
    
    def play(self):
        self.isPlay = True
    
    def next(self):
        prevPosition = self.position
        if (self.isPlay):
            self.position = (self.position + 1) % self.size
        return self.data[prevPosition]
    
    def stop(self):
        self.isPlay = False
        self.position = 0
    
    def rec(self, value):
        if (self.isPlay):
            self.data[self.position] = value
        return self.next()


class Midi:
    midiin = rtmidi.MidiIn()
    midiout = rtmidi.MidiOut()
    available_in_ports = midiin.get_ports()
    available_out_ports = midiout.get_ports()

    def __init__(self, midi_controller_in, midi_controller_out) -> None:
        self.midi_controller_in = midi_controller_in
        self.midi_controller_out = midi_controller_out
        

    def init(self):
        self.midiout.open_port(self.available_out_ports.index(self.midi_controller_out))
        self.midiin.open_port(self.available_in_ports.index(self.midi_controller_in))

    def close(self):
        self.midiin.close_port()
        self.midiout.close_port()
        
class App:
    sequencer = Sequencer(16)
    midi = Midi("MIDIIN2 (Launchkey 25) 1", "MIDIOUT2 (Launchkey 25) 2")
    lights = LauchkeyLights(midi.midiout)

    def __init__(self) -> None:
        pass

    def init(self):
        self.midi.init()
        self.lights.init()

    def poll_messages(self):
        try:
            timer = time.time()
            while True:
                msg = self.midi.midiin.get_message()

                if msg:
                    message, deltatime = msg
                    timer += deltatime
                    print("[%s] @%0.6f %r" % ("kjh",timer, message))

                time.sleep(0.001)
        except KeyboardInterrupt:
            print('')
        finally:
            print("Exit.")
            self.midi.close()
        
app = App()
app.init()
app.poll_messages()