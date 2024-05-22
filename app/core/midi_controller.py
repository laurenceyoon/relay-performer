import threading
import time

import mido
from mido import MidiFile

from ..config import CONNECTION_INTERVAL, MIDI_PORT_NAME, ADJUST_TEMPO
from ..redis import redis_client

DEFAULT_SPEED = 1


class MidiPort:
    def __init__(self, connection_interval: int):
        self.interval = connection_interval
        self.outport = None
        self.is_running = False
        print(mido.get_output_names())
        self.connect_to_midi_port()

    def connect_to_midi_port(self):
        thread = threading.Thread(target=self._connect_to_midi_port)
        thread.start()
        thread.join()

    def _connect_to_midi_port(self):
        while True:
            try:
                if self.outport is None:
                    self.outport = mido.open_output(MIDI_PORT_NAME, autoreset=True)
                    print(f"💡 MIDI PORT CONNECTED 🔌 {self.outport}")
                    break
            except Exception as e:
                print(
                    f"Failed to connect to MIDI port. Error: {e}. Retrying in {self.interval} seconds..."
                )
                time.sleep(self.interval)

    def play(self, midi: MidiFile):
        print(f"Play MIDI file: {midi.filename}")
        self.is_running = True

        # start playing
        if ADJUST_TEMPO:
            for msg in midi:
                if self.is_running:
                    if not msg.is_meta:
                        speed = float(redis_client.get("speed")) or DEFAULT_SPEED
                        time.sleep(msg.time * 1 / speed)
                        self.outport.send(msg)
                else:
                    print("Stop sending MIDI messages!")
                    return
        else:
            for msg in midi.play():
                if self.is_running:
                    self.outport.send(msg)
                else:
                    print("Stop sending MIDI messages!")
                    return

        # end of playing
        self.is_running = False

    def panic(self):
        self.is_running = False
        self.outport.panic()


midi_port = MidiPort(connection_interval=CONNECTION_INTERVAL)
