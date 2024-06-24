import time
from collections import deque

from transitions import Machine

from ..config import (
    DTW_WINDOW_SIZE,
    ENABLE_OSC,
    FEATURES,
    HOP_LENGTH,
    HUMAN_PLAYER,
    MAX_RUN_COUNT,
    METRIC,
    SAMPLE_RATE,
)
from ..models import Piece, SubPiece
from ..redis import redis_client
from .dto import Schedule
from .midi_controller import midi_port
from .online_dtw import OLTW
from .osc_connector import osc_client
from .stream_processor import sp
from .utils import get_audio_path_from_midi_path, get_midi_from_piece


class RelayPerformer:
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
        self.oltw = None

        self.machine = Machine(
            model=self, states=RelayPerformer.states, initial="asleep"
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
        return self.current_player in HUMAN_PLAYER

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
        if self.oltw is not None:
            self.oltw.stop()
        self.oltw = None

    def start_following(self):
        print(f"\n🎹 switch player to {self.current_player} 👩 🎹")
        print(f"remaining schedules count: {len(self.schedules)}")
        self.force_quit_flag = False
        print(f"start following!, current subpiece: {self.current_subpiece}")
        current_subpiece_audio_path = get_audio_path_from_midi_path(
            self.current_subpiece.path
        )

        self.oltw = OLTW(
            sp,
            ref_audio_path=current_subpiece_audio_path.as_posix(),
            window_size=DTW_WINDOW_SIZE,
            sample_rate=SAMPLE_RATE,
            hop_length=HOP_LENGTH,
            metric=METRIC,
            features=FEATURES,
            max_run_count=MAX_RUN_COUNT,
        )
        start_time = time.time()
        self.oltw.run()
        if not self.force_quit_flag:
            estimated_time_remaining = max(self.current_subpiece.etr - 0.7, 0)
            time.sleep(estimated_time_remaining)  # sleep for estimated time remaining
            print(f"duration: {time.time() - start_time}")
            self.switch()

    def start_playing(self):
        play_speed = (
            float(redis_client.get("speed"))
            if redis_client.get("speed") is not None
            else 1.0
        )
        print(
            f"""
\n🎹 switch player to {self.current_schedule.player} 🤖 🎹
Playback Speed: {play_speed}
remaining schedules count: {len(self.schedules)}"""
        )
        if self.current_subpiece.is_midi():
            self.force_quit_flag = False
            print(f"start_playing!, current subpiece: {self.current_subpiece}")
            midi = get_midi_from_piece(self.current_subpiece)
            print(f"play {self.current_subpiece} start")

            start_time = time.time()
            midi_port.play(midi)
            print(f"play {self.current_subpiece} end")
            midi_port.panic()

            print(f"duration: {time.time() - start_time}")
            self.switch()

        if ENABLE_OSC:  # Audio (MAX/MSP)
            osc_client.send_message(f"/start/{self.current_subpiece.id}")
            # switch to next schedule when receiving OSC message (helper: switch_to_next_schedule)

    def force_quit(self):
        self.force_quit_flag = True
        self.cleanup_following()
        print("Quit & cleanup completed.")
