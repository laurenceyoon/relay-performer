import queue
import threading
import time
from typing import Optional

import librosa
import numpy as np
import pyaudio
import soundfile as sf

from ..config import CHANNELS, CHUNK_SIZE, FEATURES, HOP_LENGTH, N_FFT, SAMPLE_RATE
from .utils import process_chroma, process_mfcc, process_phonemes


class StreamProcessor:
    def __init__(
        self,
        sample_rate,
        chunk_size,
        hop_length,
        n_fft,
        verbose=False,
        features=FEATURES,
    ):
        self.chunk_size = chunk_size
        self.channels = CHANNELS
        self.sample_rate = sample_rate
        self.hop_length = hop_length
        self.n_fft = n_fft
        self.verbose = verbose
        self.features = features
        self.format = pyaudio.paFloat32
        self.audio_interface: Optional[pyaudio.PyAudio] = None
        self.audio_stream: Optional[pyaudio.Stream] = None
        self.feature_buffer = queue.Queue()
        self.buffer = queue.Queue()
        self.last_chunk = None
        self.index = 0
        self.mock = False

    def _process_feature(self, y, time_info=None):
        if self.last_chunk is None:  # add zero padding at the first block
            y = np.concatenate((np.zeros(self.hop_length), y))
        else:
            # add last chunk at the beginning of the block
            # making 5 block, 1 block overlap -> 4 frames each time
            y = np.concatenate((self.last_chunk, y))

        y_feature = None
        for feature in self.features:
            if feature == "chroma":
                y_chroma = process_chroma(y)
                y_feature = (
                    y_chroma if y_feature is None else np.vstack((y_feature, y_chroma))
                )
            elif feature == "mfcc":
                y_mfcc = process_mfcc(y)
                y_feature = (
                    y_mfcc if y_feature is None else np.vstack((y_feature, y_mfcc))
                )
            elif feature == "phoneme":
                y_phoneme = process_phonemes(y)
                y_feature = (
                    y_phoneme
                    if y_feature is None
                    else np.vstack((y_feature, y_phoneme))
                )

        current_chunk = {
            "timestamp": time_info if time_info else time.time(),
            "feature": y_feature,
        }
        self.feature_buffer.put(current_chunk)
        self.last_chunk = y[-self.hop_length :]
        self.index += 1

    def _process_frame(self, data, frame_count, time_info, status_flag):
        if self.verbose:
            print(f"\nprocess_frame index: {self.index}, frame_count: {frame_count}")
            print(f"{self.index}st time_info: {time_info}")

        self.buffer.put(data)

        query_audio = np.frombuffer(data, dtype=np.float32)  # initial y
        self._process_feature(query_audio, time_info["input_buffer_adc_time"])

        return (data, pyaudio.paContinue)

    def mock_stream(self, file_path):
        duration = int(librosa.get_duration(filename=file_path))
        # time_interval = self.chunk_size / self.sample_rate  # 0.2 sec
        # time.sleep(time_interval)  # 실제 시간과 동일하게 simulation

        audio_y, _ = librosa.load(file_path, sr=self.sample_rate)
        padded_audio = np.concatenate(
            (audio_y, np.zeros(duration * 2 * self.sample_rate))
        )
        trimmed_audio = padded_audio[
            : len(padded_audio) - (len(padded_audio) % self.chunk_size)
        ]
        while trimmed_audio.any():
            audio_chunk = trimmed_audio[: self.chunk_size]
            time_info = {"input_buffer_adc_time": time.time()}
            self._process_feature(audio_chunk, time_info)
            trimmed_audio = trimmed_audio[self.chunk_size :]
            self.index += 1

        # fill empty values with zeros after stream is finished
        additional_padding_size = duration * 2 * self.sample_rate
        while additional_padding_size > 0:
            time_info = {"input_buffer_adc_time": time.time()}
            self._process_feature(
                np.zeros(self.chunk_size),
                time_info,
            )
            additional_padding_size -= self.chunk_size

    def run(self, mock=False, mock_file=""):
        if mock:  # mock processing
            print(f"* [Mocking] Loading existing audio file({mock_file})....")
            self.mock = True
            x = threading.Thread(target=self.mock_stream, args=(mock_file,))
            x.start()
            return

        # real-time processing
        self.audio_interface = pyaudio.PyAudio()
        self.audio_stream = self.audio_interface.open(
            format=self.format,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size,
            stream_callback=self._process_frame,
        )
        self.audio_stream.start_stream()
        self.start_time = self.audio_stream.get_time()
        if self.verbose:
            print("* Recording in progress....")

    def stop(self):
        if not self.mock and self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
            self.mock = False
            self.audio_interface.terminate()
            if self.verbose:
                print("Recording Stopped.")

    def save_wav(self, file_path):
        y = None
        while not self.feature_buffer.empty():
            data = self.feature_buffer.get()
            y = data if y is None else np.concatenate((y, data))
        sf.write(file_path, y, self.sample_rate, subtype="PCM_24")


sp = StreamProcessor(
    sample_rate=SAMPLE_RATE,
    chunk_size=CHUNK_SIZE,
    hop_length=HOP_LENGTH,
    n_fft=N_FFT,
)
