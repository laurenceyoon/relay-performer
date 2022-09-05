import time

from collections import deque
import librosa
from transitions import Machine

from ..models import Piece, SubPiece
from .dto import Schedule
from .utils import get_audio_path_from_midi_path, get_midi_from_piece
from .online_dtw import OnlineTimeWarping
from .midiport import midi_port
from .stream_processor import sp
from ..config import HOP_LENGTH, FRAME_RATE, HUMAN_PLAYER
from ..redis import redis_client


class InteractivePerformer:
    states = ["asleep", "following", "playing"]

    def __init__(self, piece: Piece, start_from=1):
        self.piece = piece
        self.schedules = deque(
            Schedule(player=s.player, subpiece=s.subpiece) for s in piece.schedules
        )
        for _ in range(start_from - 1):
            self.schedules.popleft()
        print(f"length of total schedules: {len(self.schedules)}")
        self.current_schedule: Schedule = self.schedules.popleft()
        self.current_player = self.current_schedule.player
        self.current_subpiece: SubPiece = self.current_schedule.subpiece

        self.machine = Machine(
            model=self, states=InteractivePerformer.states, initial="asleep"
        )
        self.machine.add_transition(
            trigger="start_performance",
            source="asleep",
            dest="following",
            conditions="is_human_pianist_playing",
            after="start_following",
        )
        self.machine.add_transition(
            trigger="move_to_next",
            source=["following", "playing"],
            dest="playing",
            unless="is_human_pianist_playing",
            before="cleanup_following",
            after="start_playing",
        )
        self.machine.add_transition(
            trigger="move_to_next",
            source=["playing", "following"],
            dest="following",
            conditions="is_human_pianist_playing",
            after="start_following",
        )
        self.machine.add_transition(
            trigger="start_performance",
            source="asleep",
            dest="playing",
            unless="is_human_pianist_playing",
            after="start_playing",
        )
        self.machine.add_transition(
            trigger="stop_performance",
            source=["following", "playing", "asleep"],
            dest="asleep",
            before="force_quit",
        )
        self.current_timestamp = 0
        self.force_quit_flag = False

    def is_human_pianist_playing(self):
        return self.current_player == HUMAN_PLAYER

    def switch(self):
        if not self.schedules or self.force_quit_flag:
            print(f"stop performance! force quit: {self.force_quit_flag}")
            self.stop_performance()
            return

        self.current_schedule = self.schedules.popleft()
        self.current_player = self.current_schedule.player
        self.current_subpiece: SubPiece = self.current_schedule.subpiece

        self.move_to_next()  # trigger

    def cleanup_following(self):
        if self.odtw is not None:
            self.odtw.stop()
        self.odtw = None

    def start_following(self):
        print("\n🎹 switch player to Pianist 👩 🎹")
        print(f"remaining schedules count: {len(self.schedules)}")
        self.force_quit_flag = False
        print(f"start following!, current subpiece: {self.current_subpiece}")
        current_subpiece_audio_path = get_audio_path_from_midi_path(
            self.current_subpiece.path
        )

        # replace alignment
        self.odtw = OnlineTimeWarping(
            sp,
            ref_audio_path=current_subpiece_audio_path.as_posix(),
            window_size=FRAME_RATE * 3,  # window size: 3 sec
            hop_length=HOP_LENGTH,
            verbose=False,
            max_run_count=3,
            ref_norm=None,
        )
        start_time = time.time()
        self.odtw.run()
        if not self.force_quit_flag:
            estimated_time_remaining = max(self.current_subpiece.etr - 0.7, 0)
            time.sleep(estimated_time_remaining)  # sleep for estimated time remaining
            print(f"duration: {time.time() - start_time}")
            self.switch()

    def start_playing(self):
        print(
            f"""\n🎹 switch player to VirtuosoNet 🤖 🎹
            \nPlayback Speed: {float(redis_client.get("speed"))}
            \nremaining schedules count: {len(self.schedules)}
            """
        )
        self.force_quit_flag = False
        print(f"start_playing!, current subpiece: {self.current_subpiece}")
        midi = get_midi_from_piece(self.current_subpiece)
        print(f"play {self.current_subpiece} start")
        start_time = time.time()
        midi_port.send(midi)
        print(f"play {self.current_subpiece} end")
        midi_port.panic()

        print(f"duration: {time.time() - start_time}")
        self.switch()

    def force_quit(self):
        self.force_quit_flag = True
        self.cleanup_following()
        print("Quit & cleanup completed.")
