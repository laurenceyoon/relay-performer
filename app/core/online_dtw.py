import time
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from functools import partial
import scipy
from tqdm import tqdm

from ..config import HOP_LENGTH, Direction, N_FFT, FRAME_RATE
from ..redis import redis_client
from .stream_processor import StreamProcessor

# matplotlib.use("agg")
MAX_LEN = int(1e4)


class OnlineTimeWarping:
    def __init__(
        self,
        sp: StreamProcessor,
        ref_audio_path,
        window_size,
        hop_length,
        max_run_count=30,
        verbose=False,
        ref_norm=None,
    ):
        self.sp = sp
        self.ref_audio_file = ref_audio_path
        self.w = window_size  # * self.frame_per_seg
        self.max_run_count = max_run_count
        self.hop_length = hop_length
        self.frame_per_seg = int(sp.chunk_size / hop_length)
        self.verbose = verbose
        self.ref_norm = ref_norm
        self.ref_pointer = 0
        self.query_pointer = 0
        self.run_count = 0
        self.previous_direction = None
        self.current_query_stft = None  # (12, n)
        self.query_stft = np.zeros((12, MAX_LEN))  # (12, N) stft of total query
        self.dist_matrix = None
        self.acc_dist_matrix = None
        self.candidate = None
        self.candi_history = [[0, 0]]
        self.iteration = 0
        self.is_running = True

        self.initialize_ref_audio(ref_audio_path)

    def offset(self):
        offset_x = max(self.ref_pointer - self.w, 0)
        offset_y = max(self.query_pointer - self.w, 0)
        return np.array([offset_x, offset_y])

    def initialize_ref_audio(self, audio_path):
        audio_y, sr = librosa.load(audio_path)
        self.ref_audio = audio_y
        ref_stft = librosa.feature.chroma_stft(
            y=audio_y, sr=sr, hop_length=HOP_LENGTH, n_fft=N_FFT, norm=self.ref_norm
        )
        ref_len = ref_stft.shape[1]
        truncated_len = (
            (ref_len - 1) // self.frame_per_seg
        ) * self.frame_per_seg  # initialize_ref_audio 에서 ref_stft 길이가 frame_per_seg (4) 로 나눠지게 마지막을 버림
        self.ref_stft = ref_stft[:, :truncated_len]
        self.ref_stft = np.log(self.ref_stft * 10 + 1) / 8
        self.ref_total_length = self.ref_stft.shape[1]

        self.global_cost_matrix = np.zeros(
            (self.ref_total_length * 2, self.ref_total_length * 2)
        )

    def init_dist_matrix(self):
        ref_stft_seg = self.ref_stft[:, : self.ref_pointer]  # [F, M]
        query_stft_seg = self.query_stft[:, : self.query_pointer]  # [F, N]
        dist = scipy.spatial.distance.cdist(ref_stft_seg.T, query_stft_seg.T)
        self.dist_matrix[self.w - dist.shape[0] :, self.w - dist.shape[1] :] = dist

    def init_matrix(self):
        x = self.ref_pointer
        y = self.query_pointer
        d = self.frame_per_seg
        wx = min(self.w, x)
        wy = min(self.w, y)
        new_acc = np.zeros((wx, wy))
        new_len_acc = np.zeros((wx, wy))
        x_seg = self.ref_stft[:, x - wx : x].T  # [wx, 12]
        y_seg = self.query_stft[:, y - d : y].T  # [d, 12]
        dist = scipy.spatial.distance.cdist(x_seg, y_seg)  # [wx, d]

        for i in range(wx):
            for j in range(d):
                local_dist = dist[i, j]
                update_x0 = 0
                update_y0 = wy - d
                if i == 0 and j == 0:
                    new_acc[i, j] = local_dist
                elif i == 0:
                    new_acc[i, update_y0 + j] = local_dist + new_acc[i, update_y0 - 1]
                    new_len_acc[i, update_y0 + j] = 1 + new_len_acc[i, update_y0 - 1]
                elif j == 0:
                    new_acc[i, update_y0 + j] = local_dist + new_acc[i - 1, update_y0]
                    new_len_acc[i, update_y0 + j] = (
                        local_dist + new_len_acc[i - 1, update_y0]
                    )
                else:
                    compares = [
                        new_acc[i - 1, update_y0 + j],
                        new_acc[i, update_y0 + j - 1],
                        new_acc[i - 1, update_y0 + j - 1] * 0.98,
                    ]
                    len_compares = [
                        new_len_acc[i - 1, update_y0 + j],
                        new_len_acc[i, update_y0 + j - 1],
                        new_len_acc[i - 1, update_y0 + j - 1],
                    ]
                    local_direction = np.argmin(compares)
                    new_acc[i, update_y0 + j] = local_dist + compares[local_direction]
                    new_len_acc[i, update_y0 + j] = 1 + len_compares[local_direction]
        self.acc_dist_matrix = new_acc
        self.acc_len_matrix = new_len_acc
        self.select_candidate()

    def update_accumulate_matrix(self, direction):
        # local cost matrix
        x = self.ref_pointer
        y = self.query_pointer
        d = self.frame_per_seg
        wx = min(self.w, x)
        wy = min(self.w, y)
        new_acc = np.zeros((wx, wy))
        new_len_acc = np.zeros((wx, wy))

        if direction is Direction.REF:
            new_acc[:-d, :] = self.acc_dist_matrix[d:]
            new_len_acc[:-d, :] = self.acc_len_matrix[d:]
            x_seg = self.ref_stft[:, x - d : x].T  # [d, 12]
            y_seg = self.query_stft[:, y - wy : y].T  # [wy, 12]
            dist = scipy.spatial.distance.cdist(x_seg, y_seg)  # [d, wy]

            for i in range(d):
                for j in range(wy):
                    local_dist = dist[i, j]
                    update_x0 = wx - d
                    update_y0 = 0
                    if j == 0:
                        new_acc[update_x0 + i, j] = (
                            local_dist + new_acc[update_x0 + i - 1, j]
                        )
                        new_len_acc[update_x0 + i, j] = (
                            new_len_acc[update_x0 + i - 1, j] + 1
                        )
                    else:
                        compares = [
                            new_acc[update_x0 + i - 1, j],
                            new_acc[update_x0 + i, j - 1],
                            new_acc[update_x0 + i - 1, j - 1] * 0.98,
                        ]
                        len_compares = [
                            new_len_acc[update_x0 + i - 1, j],
                            new_len_acc[update_x0 + i, j - 1],
                            new_len_acc[update_x0 + i - 1, j - 1],
                        ]
                        local_direction = np.argmin(compares)
                        new_acc[update_x0 + i, j] = (
                            local_dist + compares[local_direction]
                        )
                        new_len_acc[update_x0 + i, j] = (
                            1 + len_compares[local_direction]
                        )

        elif direction is Direction.QUERY:
            overlap_y = wy - d
            new_acc[:, :-d] = self.acc_dist_matrix[:, -overlap_y:]
            new_len_acc[:, :-d] = self.acc_len_matrix[:, -overlap_y:]
            x_seg = self.ref_stft[:, x - wx : x].T  # [wx, 12]
            y_seg = self.query_stft[:, y - d : y].T  # [d, 12]
            dist = scipy.spatial.distance.cdist(x_seg, y_seg)  # [wx, d``]

            for i in range(wx):
                for j in range(d):
                    local_dist = dist[i, j]
                    update_x0 = 0
                    update_y0 = wy - d
                    if i == 0:
                        new_acc[i, update_y0 + j] = (
                            local_dist + new_acc[i, update_y0 - 1]
                        )
                        new_len_acc[i, update_y0 + j] = (
                            1 + new_len_acc[i, update_y0 - 1]
                        )
                    else:
                        compares = [
                            new_acc[i - 1, update_y0 + j],
                            new_acc[i, update_y0 + j - 1],
                            new_acc[i - 1, update_y0 + j - 1] * 0.98,
                        ]
                        len_compares = [
                            new_len_acc[i - 1, update_y0 + j],
                            new_len_acc[i, update_y0 + j - 1],
                            new_len_acc[i - 1, update_y0 + j - 1],
                        ]
                        local_direction = np.argmin(compares)
                        new_acc[i, update_y0 + j] = (
                            local_dist + compares[local_direction]
                        )
                        new_len_acc[i, update_y0 + j] = (
                            1 + len_compares[local_direction]
                        )
        self.acc_dist_matrix = new_acc
        self.acc_len_matrix = new_len_acc

    def update_path_cost(self, direction):
        self.update_accumulate_matrix(direction)
        self.select_candidate()

    def select_candidate(self):
        norm_x_edge = self.acc_dist_matrix[-1, :] / self.acc_len_matrix[-1, :]
        norm_y_edge = self.acc_dist_matrix[:, -1] / self.acc_len_matrix[:, -1]
        cat = np.concatenate((norm_x_edge, norm_y_edge))
        min_idx = np.argmin(cat)
        offset = self.offset()
        if min_idx <= len(norm_x_edge):
            self.candidate = np.array([self.ref_pointer - offset[0], min_idx])
        else:
            self.candidate = np.array(
                [min_idx - len(norm_x_edge), self.query_pointer - offset[1]]
            )

    def save_history(self):
        offset = self.offset()
        self.candi_history.append(offset + self.candidate)

    def select_next_direction(self):
        if self.query_pointer <= self.w:
            next_direction = Direction.QUERY
        elif self.run_count > self.max_run_count:
            next_direction = (
                Direction.QUERY
                if self.previous_direction is Direction.REF
                else Direction.REF
            )
        else:
            offset = self.offset()
            x0 = offset[0]
            y0 = offset[1]
            if self.candidate[0] == self.ref_pointer - x0:
                next_direction = Direction.REF
            else:
                assert self.candidate[1] == self.query_pointer - y0
                next_direction = Direction.QUERY
        return next_direction

    def get_new_input(self):
        #  get only one input at a time
        query_chroma_stft = self.sp.chroma_buffer.get()["chroma_stft"]
        self.current_query_stft = query_chroma_stft
        q_length = self.current_query_stft.shape[1]
        self.query_stft[
            :, self.query_pointer : self.query_pointer + q_length
        ] = query_chroma_stft
        self.query_pointer += q_length

    def _check_run_time(self, start_time, duration):
        return time.time() - start_time < duration

    def _is_still_following(self):
        return self.ref_pointer <= (self.ref_total_length - self.frame_per_seg)

    def run(self, fig=None, h=None, hfig=None, duration=None, mock=False):
        pbar = tqdm(total=self.ref_total_length)
        self.sp.run(mock=mock)  # mic ON
        start_time = time.time()

        self.ref_pointer += self.w
        self.get_new_input()
        self.init_matrix()
        # pbar.update(self.candi_history[-1][0])
        last_ref_checkpoint = 0

        run_condition = (
            partial(self._check_run_time, start_time, duration)
            if duration is not None
            else self.sp.is_open
        )
        while self.is_running and run_condition() and self._is_still_following():
            pbar.update(self.candi_history[-1][0] - last_ref_checkpoint)
            pbar.set_description(
                f"[{self.ref_pointer}/{self.ref_total_length}] ref: {self.ref_pointer}, query: {self.query_pointer}"
            )
            last_ref_checkpoint = self.candi_history[-1][0]
            self.save_history()
            direction = self.select_next_direction()

            if direction is Direction.QUERY:
                self.get_new_input()
                self.update_path_cost(direction)

            elif direction is Direction.REF:
                self.ref_pointer += self.frame_per_seg
                self.update_path_cost(direction)

            if direction == self.previous_direction:
                self.run_count += 1
            else:
                self.run_count = 1

            self.previous_direction = direction
            self.iteration += 1

            if duration is None:
                duration = int(librosa.get_duration(filename=self.ref_audio_file)) + 1
            if h and hfig and fig:
                h.set_data(self.query_stft[:, : FRAME_RATE * duration])
                hfig.update(fig)

        if self.is_running:
            pbar.set_description(
                f"[{self.ref_pointer}/{self.ref_total_length}, {int(self.ref_pointer/self.ref_total_length*100)}%] ref: {self.ref_pointer}, query: {self.query_pointer}"
            )
            pbar.update(
                self.candi_history[-1][0] - last_ref_checkpoint + self.frame_per_seg
            )
            self.stop()
            redis_client.get("speed", self.ref_total_length / self.query_pointer)

    def stop(self):
        self.is_running = False
        self.sp.stop()
