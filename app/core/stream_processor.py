import librosa
import numpy as np
import pyaudio
import queue
from typing import Optional
import time

from ..config import CHUNK_SIZE, HOP_LENGTH, SAMPLE_RATE, CHANNELS, N_FFT


class StreamProcessor:
    def __init__(
        self, sample_rate, chunk_size, hop_length, n_fft, verbose=False, query_norm=None
    ):
        self.chunk_size = chunk_size
        self.channels = CHANNELS
        self.sample_rate = sample_rate
        self.hop_length = hop_length
        self.n_fft = n_fft
        self.verbose = verbose
        self.query_norm = query_norm
        self.format = pyaudio.paFloat32
        self.audio_interface: Optional[pyaudio.PyAudio] = None
        self.audio_stream: Optional[pyaudio.Stream] = None
        self.buffer = queue.Queue()
        self.chroma_buffer = queue.Queue()
        self.last_chunk = None
        self.is_mic_open = False
        self.index = 0

    def _process_chroma(self, y, time_info=None):
        y = np.concatenate((self.last_chunk, y)) if self.last_chunk is not None else y
        query_chroma_stft = (
            librosa.feature.chroma_stft(  # TODO: center = False 옵션 줘서 해보기
                y=y,
                sr=self.sample_rate,
                hop_length=self.hop_length,
                n_fft=self.n_fft,
                norm=self.query_norm,
            )
        )
        # 첫번째 chunk 는 맨 앞의 padding된 stft frame을 버리지 않음
        query_chroma_stft = (
            query_chroma_stft[:, 1:-1]
            if self.last_chunk is not None
            else query_chroma_stft[:, :-1]
        )
        query_chroma_stft = np.log(query_chroma_stft * 5 + 1) / 16
        current_chunk = {
            "timestamp": time_info if time_info else time.time(),
            "chroma_stft": query_chroma_stft,
        }
        self.chroma_buffer.put(current_chunk)
        self.last_chunk = y[y.shape[0] - self.hop_length :]
        self.index += 1

    def _process_frame(self, data, frame_count, time_info, status_flag):
        if self.verbose:
            print(f"\nprocess_frame index: {self.index}, frame_count: {frame_count}")
            print(f"{self.index}st time_info: {time_info}")

        self.buffer.put(data)

        query_audio = np.frombuffer(data, dtype=np.float32)  # initial y
        self._process_chroma(query_audio, time_info["input_buffer_adc_time"])

        return (data, pyaudio.paContinue)

    def mock_stream(self, mock_file=None):
        filename = (
            mock_file
            or "../resources/audio/target/presto_musescore/Haydn_Hob._XVI34_1._Presto.wav"
        )
        stream = librosa.stream(
            filename,
            block_length=int(self.chunk_size / self.hop_length),
            frame_length=self.chunk_size,
            hop_length=self.hop_length,
        )
        for y_block in stream:
            print(f"y_block.shape: {y_block.shape}")
            self._process_chroma(y_block)

    def run(self, mock=False, mock_file=None):
        if mock:
            print(f"* [Mocking] Loading existing audio file({mock_file})....")
            self.mock_stream(mock_file)
            print("* [Mocking] Done.")
        else:
            self.audio_interface = pyaudio.PyAudio()
            self.audio_stream = self.audio_interface.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size,
                stream_callback=self._process_frame,
            )
            self.is_mic_open = True
            self.audio_stream.start_stream()
            self.start_time = self.audio_stream.get_time()
            if self.verbose:
                print("* Recording in progress....")

    def stop(self):
        if self.is_mic_open:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
            self.is_mic_open = False
            self.audio_interface.terminate()
            if self.verbose:
                print("Recording Stopped.")

    def is_open(self):
        return self.is_mic_open


sp = StreamProcessor(
    sample_rate=SAMPLE_RATE,
    chunk_size=CHUNK_SIZE,
    hop_length=HOP_LENGTH,
    n_fft=N_FFT,
    query_norm=None,
)
