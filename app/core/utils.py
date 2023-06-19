from pathlib import Path
import mido
import numpy as np
import librosa
import torch
from attributedict.collections import AttributeDict

from ..model.model import CRNN
from ..config import SAMPLE_RATE, HOP_LENGTH, N_FFT, NORM, CRNN_MODEL_PATH

save_data = torch.load(CRNN_MODEL_PATH, map_location="mps")
model_state_dict = save_data["model_state_dict"]
config = AttributeDict(save_data["config"])
consts = AttributeDict(save_data["consts"])
config.device = "mps"

crnn_model = CRNN(config, consts)
crnn_model.to("mps")

crnn_model.load_state_dict(model_state_dict, strict=False)
crnn_model.eval()


def get_audio_path_from_midi_path(midi_path):
    audio_dir = Path("./resources/audio/")
    audio_path = audio_dir / f"{Path(midi_path).stem}.wav"
    return audio_path


def get_midi_from_piece(piece) -> mido.MidiFile:
    return mido.MidiFile(piece.path)


def softmax_with_temperature(z, T=1):
    y = np.exp(z / T) / np.sum(np.exp(z / T), axis=0)
    return y


def scale_with_sigmoid(x):
    return 1 / (1 + np.exp(-x))


def process_chroma(y, sr=SAMPLE_RATE, hop_length=HOP_LENGTH, n_fft=N_FFT, norm=NORM):
    chroma_stft = librosa.feature.chroma_stft(
        y=y,
        sr=sr,
        hop_length=hop_length,
        n_fft=n_fft,
        norm=norm,
        center=False,
    )
    # chroma_stft = np.log1p(chroma_stft * 5) / 4
    chroma_stft = scale_with_sigmoid((chroma_stft - 0.5) * 10)
    return chroma_stft


def process_phonemes(y):
    # if not real_time:
    #     padding = np.zeros(HOP_LENGTH)
    #     y = np.concatenate((padding, y, padding))

    x_tensor = torch.from_numpy(y).float().to("mps")

    with torch.no_grad():
        batch = dict()
        batch["audio"] = x_tensor.unsqueeze(0)
        predictions = crnn_model.run_on_batch(batch, cal_loss=False)

    phonemes = predictions["frame"].squeeze().T.cpu().numpy()  # [39, T]
    phonemes = phonemes[:, 1:-1]  # remove <sos> and <eos>
    phonemes = softmax_with_temperature(phonemes, T=1)
    phonemes = np.log1p(phonemes * 5) / 4
    return phonemes
