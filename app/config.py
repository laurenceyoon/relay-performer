from pathlib import Path

import numpy as np

CHANNELS = 1
SAMPLE_RATE = 22050
HOP_LENGTH = 512
CHUNK_SIZE = 4 * HOP_LENGTH
N_FFT = 2 * HOP_LENGTH
FRAME_RATE = int(SAMPLE_RATE / HOP_LENGTH)  # 1초당 프레임 개수
DTW_WINDOW_SIZE = int(3 * FRAME_RATE)  # 3초
FEATURES = ["chroma"]  # chroma, mel, phoneme
METRIC = "cosine"
NORM = np.inf

# config for MIDI Port
MIDI_PORT_NAME = None  # "USB MIDI" or None
CONNECTION_INTERVAL = 5

# config for CRNN classifier model
CRNN_MODEL_PATH = Path("./app/model/uni-5cls-640hop.pt")
N_MELS = 66

# config for RelayPerformer
AI_PLAYER = "VirtuosoNet"
HUMAN_PLAYER = "Pianist"
ENABLE_OSC = True
ADJUST_TEMPO = False

# config for OSC connection
OSC_CLIENT_IP = "127.0.0.1"
OSC_CLIENT_PORT = 53000
