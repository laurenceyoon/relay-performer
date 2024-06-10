from pathlib import Path

import numpy as np

CHANNELS = 1
SAMPLE_RATE = 22050
HOP_LENGTH = 512
CHUNK_SIZE = HOP_LENGTH
N_FFT = 2 * HOP_LENGTH
N_MFCC = 5
FRAME_RATE = int(SAMPLE_RATE / HOP_LENGTH)  # 1초당 프레임 개수
DTW_WINDOW_SIZE = int(2 * FRAME_RATE)
MAX_RUN_COUNT = 30
FEATURES = ["chroma"]  # chroma, mel, phoneme
METRIC = "cosine"
NORM = np.inf

# config for MIDI Port ("USB MIDI", "YAMAHA USB Device Port1" or None)
MIDI_PORT_NAME = None
CONNECTION_INTERVAL = 5

# config for CRNN classifier model
USE_TORCH = "phoneme" in FEATURES
CRNN_MODEL_PATH = Path("./app/model/uni-5cls-640hop.pt")
N_MELS = 66

# config for RelayPerformer
AI_PLAYER = "VirtuosoNet"
HUMAN_PLAYER = ["Pianist", "Human"]
ADJUST_TEMPO = False

# config for OSC connection
ENABLE_OSC = False
OSC_CLIENT_IP = "127.0.0.1"
OSC_CLIENT_PORT = 53000
