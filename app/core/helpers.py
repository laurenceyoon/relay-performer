import asyncio
import matplotlib.pyplot as plt

import numpy as np

from ..models import Piece, Schedule
from .midiport import midi_port
from .stream_processor import sp
from .interactive_performer import InteractivePerformer
from .utils import get_midi_from_piece

interactive_performer = None


def play_piece_to_outport(piece: Piece):
    midi = get_midi_from_piece(piece)
    print(f"* Playing piece({piece.title}) start...")
    midi_port.send(midi)
    print(f"* Playing piece({piece.title}) Ended.")


def set_playback_speed(speed: float):
    print(f"############ Set playback speed to {speed} ############")
    midi_port.speed = speed


def all_stop_playing():
    print("############ all stop playing ############")
    midi_port.panic()
    if interactive_performer is not None:
        interactive_performer.stop_performance()


def open_stream():
    print("############ open audio stream ############")
    sp.run()


def close_stream():
    print("############ stop audio stream ############")
    sp.stop()


async def waiter(schedule: Schedule, event: asyncio.Event):
    print(f"Starting waiting for the last measure's start time")
    await event.wait()
    print(f"Wait FINISHED! waiting for sleep for the target measure to start")
    await asyncio.sleep(1.5)
    print(f"LET'S PLAY!")
    play_piece_to_outport(schedule.subpiece)


def load_piece_for_interactive_performance(piece: Piece, start_from=1):
    global interactive_performer
    interactive_performer = InteractivePerformer(piece=piece, start_from=start_from)


def start_interactive_performance(piece: Piece, start_from=1):
    load_piece_for_interactive_performance(piece, start_from)
    print(f"\n🎹 Let's play! {piece.title} 🎹")
    interactive_performer.start_performance()


def get_current_state():
    return (
        interactive_performer.state
        if interactive_performer is not None
        else "Not Initialized"
    )


def plot_path(odtw, query_cqt, query_cqt_mag, ref_cqt, ref_cqt_mag, path):
    plt.figure(figsize=(9, 8))

    # Bottom right plot.
    ax1 = plt.axes([0.2, 0, 0.8, 0.20])
    ax1.imshow(
        query_cqt_mag,
        origin="lower",
        aspect="auto",
        cmap="magma",
    )
    ax1.set_xlabel("Real Time Performance (Query)")
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_ylim(20)

    # Top left plot.
    ax2 = plt.axes([0, 0.2, 0.20, 0.8])
    ax2.imshow(
        ref_cqt_mag.T[:, ::-1],
        origin="lower",
        aspect="auto",
        cmap="magma",
    )
    ax2.set_ylabel("Reference Signal (Synthesized)")
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.set_ylim(20)

    # Top right plot.
    ax3 = plt.axes([0.2, 0.2, 0.8, 0.8], sharex=ax1, sharey=ax2)
    ax3.imshow(
        odtw.cost_matrix,
        aspect="auto",
        origin="lower",
        interpolation="nearest",
        cmap="gray",
    )
    ax3.set_xticks([])
    ax3.set_yticks([])

    # Path.
    ax3.plot(np.flip(odtw.warping_path)[:, 0], np.flip(odtw.warping_path)[:, 1], "r")
    plt.savefig("F1.png")

    ### SECOND PLOT
    print(
        f"BEFORE SECOND PLOT, warping_path shape: {odtw.warping_path.shape}, 1st: {odtw.warping_path[0]}"
    )
    print(f"ref cens: {odtw.ref_stft.shape}, query cens: {odtw.query_stft.shape}")

    plt.figure(figsize=(11, 5))

    # Top plot.
    ax1 = plt.axes([0, 0.60, 1, 0.40])
    ax1.imshow(ref_cqt_mag, origin="lower", aspect="auto", cmap="magma")
    ax1.set_ylabel("Reference Signal (Synthesized)")
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_ylim(20)
    ax1.set_xlim(0, ref_cqt.shape[1])

    # Bottom plot.
    ax2 = plt.axes([0, 0, 1, 0.40])
    ax2.imshow(query_cqt_mag, origin="lower", aspect="auto", cmap="magma")
    ax2.set_ylabel("Query Signal (Performance)")
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.set_ylim(20)
    ax2.set_xlim(0, query_cqt.shape[1])

    # Middle plot.
    line_color = "k"
    step = 30
    n1 = float(ref_cqt.shape[1])
    n2 = float(query_cqt.shape[1])
    ax3 = plt.axes([0, 0.40, 1, 0.20])
    for query, ref in path[::step]:
        ax3.plot((ref / n1, query / n2), (1, -1), color=line_color)
        ax3.set_xlim(0, 1)
        ax3.set_ylim(-1, 1)

    # Path markers on top and bottom plot.
    y1_min, y1_max = ax1.get_ylim()
    y2_min, y2_max = ax2.get_ylim()

    ax1.vlines([t[1] for t in path[::step]], y1_min, y1_max, color=line_color)
    ax2.vlines([t[0] for t in path[::step]], y2_min, y2_max, color=line_color)
    ax3.set_xticks([])
    ax3.set_yticks([])

    plt.savefig("F2.png")
