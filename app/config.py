from enum import IntEnum
from pathlib import Path
import numpy as np


CHANNELS = 1
SAMPLE_RATE = 16000
HOP_LENGTH = 640
CHUNK_SIZE = 4 * HOP_LENGTH
N_FFT = 2 * HOP_LENGTH
FRAME_RATE = SAMPLE_RATE / HOP_LENGTH  # 1초당 25 프레임
DTW_WINDOW_SIZE = int(3 * FRAME_RATE)  # 3초
FEATURES = ["chroma", "phoneme"]  # chroma, mel, phoneme
METRIC = "cosine"
NORM = np.inf

# config for CRNN classifier model
CRNN_MODEL_PATH = Path("./app/model/uni-5cls-640hop.pt")
N_MELS = 66

SOUND_FONT_PATH = "~/Library/Audio/Sounds/Banks/GeneralUser\ GS\ v1.471.sf2"
AI_PLAYER = "VirtuosoNet"
HUMAN_PLAYER = "Pianist"
