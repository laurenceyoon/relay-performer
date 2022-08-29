from pathlib import Path
import mido


def get_audio_path_from_midi_path(midi_path):
    audio_dir = Path("./resources/audio/target/")
    audio_path = audio_dir / f"{Path(midi_path).stem}.wav"
    return audio_path

def get_midi_from_piece(piece) -> mido.MidiFile:
    return mido.MidiFile(piece.path)
