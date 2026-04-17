\import os
import numpy as np
import matplotlib.pyplot as plt
import requests

from moviepy.editor import VideoClip, AudioFileClip, ImageClip, CompositeVideoClip

# -------------------------
# PATH SETUP
# -------------------------
BASE_DIR = "powerpoint"

def path(x):
    return os.path.join(BASE_DIR, x)

# -------------------------
# LOCAL ASSETS
# -------------------------
ninja_file = path("ninja.png")
tenpin_file = path("tenpin.png")

five_file = path("five.png")
ten_file = path("ten.png")
twenty_file = path("twenty.png")

drum_file = path("drumroll.mp3")

# -------------------------
# DRUMROLL (WEB + FALLBACK)
# -------------------------
drum_url = "https://cdn.pixabay.com/download/audio/2022/03/15/audio_7c2f8c2a7e.mp3?filename=drum-roll-1-16689.mp3"

def get_drumroll():
    try:
        r = requests.get(drum_url, timeout=10)
        r.raise_for_status()
        with open(drum_file, "wb") as f:
            f.write(r.content)
        print("Drumroll downloaded")
    except Exception as e:
        print("Drumroll failed → using silence:", e)
        from moviepy.audio.AudioClip import AudioArrayClip
        silence = np.zeros((int(44100 * 6), 2))
        AudioArrayClip(silence, fps=44100).write_audiofile(drum_file)

get_drumroll()

# -------------------------
# DATA
# -------------------------
classes = [f"Class {i}" for i in range(4, 16)]
values = [100,150,120,180,200,170,220,250,240,260,230,300]
duration = 6

# -------------------------
# ANIMATION FRAME
# -------------------------
def make_frame(t):
    progress = min(t / duration, 1)
    vals = [v * progress for v in values]

    fig, ax = plt.subplots(figsize=(10,6))
    fig.patch.set_facecolor("#0b3d91")
    ax.set_facecolor("#0b3d91")

    ax.barh(classes, vals, color="#4FC3F7")
    ax.set_xlim(0, max(values) * 1.2)
    ax.tick_params(colors="white")

    for spine in ax.spines.values():
        spine.set_visible(False)

    for i, v in enumerate(vals):
        ax.text(v + 2, i, f"£{int(v)}", color="white", va="center")

    plt.tight_layout()
    fig.canvas.draw()

    img = np.asarray(fig.canvas.buffer_rgba())[:, :, :3]
    plt.close(fig)
    return img

chart = VideoClip(make_frame, duration=duration)

# -------------------------
# IMAGES
# -------------------------
five = ImageClip(five_file).set_duration(duration).resize(height=120).set_position((40,150))
ten = ImageClip(ten_file).set_duration(duration).resize(height=120).set_position((60,260))
twenty = ImageClip(twenty_file).set_duration(duration).resize(height=120).set_position((50,370))

ninja = ImageClip(ninja_file).set_duration(duration).resize(height=60).set_position((800,120))
tenpin = ImageClip(tenpin_file).set_duration(duration).resize(height=60).set_position((800,220))

# -------------------------
# PANEL
# -------------------------
def make_panel():
    fig, ax = plt.subplots(figsize=(4,6))
    fig.patch.set_facecolor("#0b3d91")
    ax.set_facecolor("#0b3d91")
    ax.axis("off")

    ax.text(0.1,0.8,"🥇 1st: Ninja Warriors",color="gold",fontsize=16,transform=ax.transAxes)
    ax.text(0.1,0.6,"🥈 2nd: Tenpin",color="silver",fontsize=16,transform=ax.transAxes)
    ax.text(0.1,0.4,"🥉 3rd: Soft Play",color="#cd7f32",fontsize=16,transform=ax.transAxes)

    fig.canvas.draw()
    img = np.asarray(fig.canvas.buffer_rgba())[:, :, :3]
    plt.close(fig)
    return img

panel = ImageClip(make_panel()).set_duration(duration).set_position(("right","center"))

# -------------------------
# COMPOSITE VIDEO
# -------------------------
video = CompositeVideoClip([
    chart,
    five, ten, twenty,
    ninja,
    tenpin,
    panel
])

# -------------------------
# AUDIO
# -------------------------
audio = AudioFileClip(drum_file).subclip(0, duration)
video = video.set_audio(audio)

# -------------------------
# EXPORT
# -------------------------
video.write_videofile(path("final_slide.mp4"), fps=24)