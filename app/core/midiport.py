import mido
import time

from mido import MidiFile


class MidiPort:
    def __init__(self):
        self.outport = None
        self.is_running = False
        self.speed = 1
        try:
            outport = mido.open_output()
        except OSError:
            pass
        else:
            self.outport = outport

    def send(self, midi: MidiFile):
        self.speed = 1
        if self.outport is None:
            self.outport = mido.open_output()
        self.is_running = True

        # start playing
        # midi.ticks_per_beat = 240
        for msg in midi:
            if self.is_running:
                if not msg.is_meta:
                    time.sleep(msg.time * 1/self.speed)
                    self.outport.send(msg)
            else:
                print("Stop sending MIDI messages!")
                return
        # for msg in midi.play():
        #     if self.is_running:
        #         self.outport.send(msg)
        #     else:
        #         print("Stop sending MIDI messages!")
        #         return
        # end of playing
        self.is_running = False

    def panic(self):
        self.is_running = False
        self.outport.panic()


midi_port = MidiPort()
