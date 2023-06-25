# %%
import librosa
import librosa.display
import pyaudio
import queue
from typing import Optional
import numpy as np
import time
import matplotlib.pyplot as plt
import datetime
from collections import deque
import IPython.display
from IPython.display import clear_output
from functools import partial
import scipy
from app.core.stream_processor import sp
from app.core.online_dtw import OLTW
from app.config import *

# %%
ref_audio_path = "./resources/audio/Haydn_Hob.XVI34_1-1.wav"
duration = int(librosa.get_duration(filename=ref_audio_path)) + 1

import traceback

odtw = OLTW(
    sp,
    ref_audio_path=ref_audio_path,
    window_size=DTW_WINDOW_SIZE,  # window size: 3 sec
    sample_rate=SAMPLE_RATE,
    hop_length=HOP_LENGTH,
    max_run_count=3,
    metric=METRIC,
    features=FEATURES,
)
fig = plt.figure()
ax = fig.gca()
hfig = display(fig, display_id=True)
h = ax.imshow(
    np.zeros((12, int(SAMPLE_RATE / HOP_LENGTH) * duration)),
    aspect="auto",
    vmin=0,
    vmax=1,
    interpolation="nearest",
)

try:
    odtw.run(fig, h, hfig)

except Exception as e:
    print(f"error! : {str(e)}, {type(e)}")
    traceback.print_tb(e.__traceback__)
    sp.stop()
    pass

# %%
# visualize two sequences
x = odtw.ref_pointer
y = odtw.target_pointer
d = odtw.frame_per_seg
wx = min(odtw.w, x)
wy = min(odtw.w, y)
new_acc = np.zeros((wx, wy))
new_len_acc = np.zeros((wx, wy))

x_seg = odtw.ref_features[:, x - d : x].T  # [d, 12]
y_seg = odtw.target_features[:, y - wy : y].T  # [wy, 12]

max_step = np.max((odtw.ref_pointer, odtw.target_pointer))
# max_step = np.min((odtw.ref_pointer, odtw.query_pointer))
plt.subplot(211)
plt.imshow(odtw.ref_features[:, : odtw.ref_pointer], aspect="auto", vmin=0, vmax=0.8)
plt.xlim(0, max_step)
plt.colorbar()
plt.subplot(212)
plt.imshow(
    odtw.target_features[:, : odtw.target_pointer], aspect="auto", vmin=0, vmax=0.8
)
plt.xlim(0, max_step)
plt.colorbar()

# %%
# Visualize OLTW path
dist = scipy.spatial.distance.cdist(
    odtw.ref_features.T, odtw.target_features[:, : odtw.target_pointer].T, metric=METRIC
)  # [d, wy]
plt.figure(figsize=(20, 20))
plt.imshow(dist.T, aspect="auto", origin="lower", interpolation="nearest")
x, y = zip(*odtw.candi_history)

from matplotlib import cm

cmap = cm.get_cmap("magma", 100)
for n in range(len(x)):
    plt.plot(x[n], y[n], ".", color="r")

# %%
