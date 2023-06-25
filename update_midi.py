# %%
import mido
from mido import MidiFile, MidiTrack

# %%
file_path = "./resources/midi/subpieces/avemaria_2.mid"
midi_file = MidiFile(file_path)
msg_list = []
for msg in midi_file.tracks[0]:
    if not msg.is_meta:
        msg.channel = 0
    msg_list.append(msg)

mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

for msg in msg_list:
    track.append(msg)

mid.save("test.mid")

# %%
