import os
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image

# MoviePy import (1.0.3 compatible)
from moviepy.editor import VideoClip, AudioFileClip, ImageClip, CompositeVideoClip

# -----------------------
# PATH SETUP
# -----------------------
BASE_DIR = "powerpoint"

def path(file):
    return os.path.join(BASE_DIR, file)

# -----------------------
# FIX PIL (ANTIALIAS ERROR FIX)
# -----------------------
if not hasattr(Image, "ANTIALIAS"):
    Image.ANTIALIAS = Image.Resampling.LANCZOS

# -----------------------
# ASSUMED LOCAL FILES
# -----------------------
ninja_file = path("ninja.png")
drumroll_file = path("drumroll.mp3")

# If these exist locally, keep them in powerpoint/
five_file = path("five.png")
ten_file = path("ten.png")
twenty_file = path("twenty.png")
tenpin_file = path("tenpin.png")

# -----------------------
# DATA
# -----------------------
classes = [f"Class {i}" for i in range(4, 16)]
values = [100,150,120,180,200,170,220,250,240,260,230,300]
duration = 6

# -----------------------
# BAR CHART ANIMATION
# -----------------------
def make_frame(t):
    progress = min(t / duration, 1)
    current_values = [v * progress for v in values]

    fig, ax = plt.subplots(figsize=(10, 6))
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

    # SAFE RGBA extraction (NO tostring_rgb crash)
    img = np.asarray(fig.canvas.buffer_rgba())
    plt.close(fig)

    return img

chart = VideoClip(make_frame, duration=duration)

# -----------------------
# LEFT IMAGES (LOCAL)
# -----------------------
five = ImageClip(five_file).set_duration(duration).resize(height=120).set_position((40,150))
ten = ImageClip(ten_file).set_duration(duration).resize(height=120).set_position((60,260))
twenty = ImageClip(twenty_file).set_duration(duration).resize(height=120).set_position((50,370))

# -----------------------
# RIGHT PANEL
# -----------------------
def make_panel():
    fig, ax = plt.subplots(figsize=(4, 6))
    fig.patch.set_facecolor('#0b3d91')
    ax.set_facecolor('#0b3d91')
    ax.axis('off')

    ax.text(0.1, 0.8, "🥇 1st: Ninja Warriors", color='gold', fontsize=16, transform=ax.transAxes)
    ax.text(0.1, 0.6, "🥈 2nd: Tenpin", color='silver', fontsize=16, transform=ax.transAxes)
    ax.text(0.1, 0.4, "🥉 3rd: Soft Play", color='#cd7f32', fontsize=16, transform=ax.transAxes)

    fig.canvas.draw()
    img = np.asarray(fig.canvas.buffer_rgba())
    plt.close(fig)
    return img

panel = ImageClip(make_panel()).set_duration(duration).set_position(("right", "center"))

# -----------------------
# LOGOS (LOCAL NINJA)
# -----------------------
ninja = ImageClip(ninja_file).set_duration(duration).resize(height=60).set_position((800, 120))
tenpin = ImageClip(tenpin_file).set_duration(duration).resize(height=60).set_position((800, 220))

# -----------------------
# COMPOSITE VIDEO
# -----------------------
video = CompositeVideoClip([
    chart,
    five, ten, twenty,
    panel,
    ninja, tenpin
])

# -----------------------
# AUDIO (LOCAL DRUMROLL)
# -----------------------
audio = AudioFileClip(drumroll_file).subclip(0, duration)
video = video.set_audio(audio)

# -----------------------
# EXPORT
# -----------------------
output = path("final_slide.mp4")
video.write_videofile(output, fps=24)