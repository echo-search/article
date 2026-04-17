import os
import numpy as np
import matplotlib.pyplot as plt
import requests

from moviepy.editor import VideoClip, AudioFileClip, ImageClip, CompositeVideoClip

# -------------------------
# SETUP PATHS
# -------------------------
BASE_DIR = "powerpoint"
os.makedirs(BASE_DIR, exist_ok=True)

def path(file):
    return os.path.join(BASE_DIR, file)

# -------------------------
# SAFE DOWNLOAD (NO CRASH)
# -------------------------
def download(url, filename):
    filepath = path(filename)
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        r.raise_for_status()
        with open(filepath, "wb") as f:
            f.write(r.content)
        print(f"Downloaded {filename}")
    except Exception as e:
        print(f"Failed download: {filename} -> {e}")

# -------------------------
# ASSETS
# -------------------------

# YOU ALREADY HAVE THIS LOCAL FILE:
# powerpoint/ninja.png

ninja_path = path("ninja.png")

# SAFE WEB ASSETS
download("https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Bowling_pins_icon.svg/512px-Bowling_pins_icon.svg.png", "tenpin.png")

download("https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Bank_of_England_%C2%A35_note.jpg/512px-Bank_of_England_%C2%A35_note.jpg", "five.png")
download("https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Bank_of_England_%C2%A310_note.jpg/512px-Bank_of_England_%C2%A310_note.jpg", "ten.png")
download("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Bank_of_England_%C2%A320_note.jpg/512px-Bank_of_England_%C2%A320_note.jpg", "twenty.png")

download("https://www.soundjay.com/misc/sounds/drum-roll-1.mp3", "drumroll.mp3")

# -------------------------
# DATA
# -------------------------
classes = [f"Class {i}" for i in range(4, 16)]
values = [100,150,120,180,200,170,220,250,240,260,230,300]
duration = 6

# -------------------------
# FIXED MATPLOTLIB RENDER (NO tostring_rgb)
# -------------------------
def make_frame(t):
    progress = min(t / duration, 1)
    current_values = [v * progress for v in values]

    fig, ax = plt.subplots(figsize=(10,6))
    fig.patch.set_facecolor('#0b3d91')
    ax.set_facecolor('#0b3d91')

    ax.barh(classes, current_values, color='#4FC3F7')
    ax.set_xlim(0, max(values)*1.2)
    ax.tick_params(colors='white')

    for spine in ax.spines.values():
        spine.set_visible(False)

    for i, v in enumerate(current_values):
        ax.text(v + 2, i, f"£{int(v)}", color='white', va='center')

    plt.tight_layout()
    fig.canvas.draw()

    # SAFE conversion (works on modern matplotlib)
    image = np.asarray(fig.canvas.buffer_rgba())
    image = image[:, :, :3]  # drop alpha for MoviePy
    plt.close(fig)

    return image

chart = VideoClip(make_frame, duration=duration)

# -------------------------
# MONEY IMAGES
# -------------------------
five = ImageClip(path("five.png")).set_duration(duration).resize(height=120).set_position((40,150))
ten = ImageClip(path("ten.png")).set_duration(duration).resize(height=120).set_position((60,260))
twenty = ImageClip(path("twenty.png")).set_duration(duration).resize(height=120).set_position((50,370))

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
    img = np.asarray(fig.canvas.buffer_rgba())
    img = img[:, :, :3]
    plt.close(fig)
    return img

panel = ImageClip(make_panel()).set_duration(duration).set_position(("right","center"))

# -------------------------
# LOGOS
# -------------------------
ninja = ImageClip(ninja_path).set_duration(duration).resize(height=60).set_position((800,120))
tenpin = ImageClip(path("tenpin.png")).set_duration(duration).resize(height=60).set_position((800,220))

# -------------------------
# COMPOSITE VIDEO
# -------------------------
video = CompositeVideoClip([
    chart,
    five, ten, twenty,
    panel,
    ninja, tenpin
])

# AUDIO
audio = AudioFileClip(path("drumroll.mp3")).subclip(0, duration)
video = video.set_audio(audio)

# OUTPUT
video.write_videofile(path("final_slide.mp4"), fps=24)