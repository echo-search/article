import os
import numpy as np
import matplotlib.pyplot as plt
import requests

from moviepy.editor import VideoClip, AudioFileClip, ImageClip, CompositeVideoClip

# -------------------------
# PATH SETUP
# -------------------------
BASE_DIR = "powerpoint"
os.makedirs(BASE_DIR, exist_ok=True)

def path(file):
    return os.path.join(BASE_DIR, file)

# -------------------------
# DOWNLOAD ONLY DRUMROLL
# -------------------------
def download(url, filename):
    filepath = path(filename)
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    r.raise_for_status()
    with open(filepath, "wb") as f:
        f.write(r.content)
    return filepath

drumroll_file = download(
    "https://cdn.pixabay.com/download/audio/2022/03/15/audio_7c2f8c2a7e.mp3?filename=drum-roll-1-16689.mp3",
    "drumroll.mp3"
)

# -------------------------
# LOCAL ASSETS (YOU PROVIDE THESE)
# -------------------------
ninja_file = path("ninja.png")
tenpin_file = path("tenpin.png")
five_file = path("five.png")
ten_file = path("ten.png")
twenty_file = path("twenty.png")

# -------------------------
# DATA
# -------------------------
classes = [f"Class {i}" for i in range(4, 16)]
values = [100,150,120,180,200,170,220,250,240,260,230,300]
duration = 6

# -------------------------
# BAR CHART ANIMATION
# -------------------------
def make_frame(t):
    progress = min(t / duration, 1)
    current_values = [v * progress for v in values]

    fig, ax = plt.subplots(figsize=(10,6))
    fig.patch.set_facecolor('#0b3d91')
    ax.set_facecolor('#0b3d91')

    ax.barh(classes, current_values, color='#4FC3F7')
    ax.set_xlim(0, max(values) * 1.2)
    ax.tick_params(colors='white')

    for spine in ax.spines.values():
        spine.set_visible(False)

    for i, v in enumerate(current_values):
        ax.text(v + 2, i, f"£{int(v)}", color='white', va='center')

    plt.tight_layout()
    fig.canvas.draw()

    frame = np.asarray(fig.canvas.buffer_rgba())  # FIXED (no tostring_rgb)
    plt.close(fig)

    return frame

chart = VideoClip(make_frame, duration=duration)

# -------------------------
# IMAGE CLIPS (FIXED RESIZE)
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
    fig.patch.set_facecolor('#0b3d91')
    ax.set_facecolor('#0b3d91')
    ax.axis('off')

    ax.text(0.1,0.8,"🥇 1st: Ninja Warriors",color='gold',fontsize=16,transform=ax.transAxes)
    ax.text(0.1,0.6,"🥈 2nd: Tenpin",color='silver',fontsize=16,transform=ax.transAxes)
    ax.text(0.1,0.4,"🥉 3rd: Soft Play",color='#cd7f32',fontsize=16,transform=ax.transAxes)

    fig.canvas.draw()
    frame = np.asarray(fig.canvas.buffer_rgba())
    plt.close(fig)
    return frame

panel = ImageClip(make_panel()).set_duration(duration).set_position(("right","center"))

# -------------------------
# COMPOSITE VIDEO
# -------------------------
video = CompositeVideoClip([
    chart,
    five, ten, twenty,
    panel,
    ninja, tenpin
])

# -------------------------
# AUDIO
# -------------------------
audio = AudioFileClip(drumroll_file).subclip(0, duration)
video = video.set_audio(audio)

# -------------------------
# EXPORT
# -------------------------
video.write_videofile(path("final_slide.mp4"), fps=24)