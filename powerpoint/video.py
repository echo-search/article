import numpy as np
import matplotlib.pyplot as plt
import requests
from moviepy.editor import VideoClip, AudioFileClip, ImageClip, CompositeVideoClip

# =========================
# AUTO DOWNLOAD FILES
# =========================
def download(url, filename):
    r = requests.get(url)
    with open(filename, "wb") as f:
        f.write(r.content)

# Logos + money + sound
download("https://www.kindpng.com/picc/m/83-832850_american-ninja-warrior-logo-png-american-ninja-warrior.png", "ninja.png")
download("https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Bowling_pins_icon.svg/512px-Bowling_pins_icon.svg.png", "tenpin.png")

download("https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Bank_of_England_%C2%A35_note.jpg/512px-Bank_of_England_%C2%A35_note.jpg", "five.png")
download("https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Bank_of_England_%C2%A310_note.jpg/512px-Bank_of_England_%C2%A310_note.jpg", "ten.png")
download("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Bank_of_England_%C2%A320_note.jpg/512px-Bank_of_England_%C2%A320_note.jpg", "twenty.png")

download("https://www.soundjay.com/misc/sounds/drum-roll-1.mp3", "drumroll.mp3")

# =========================
# DATA (EDIT VALUES ONLY)
# =========================
classes = [f"Class {i}" for i in range(4, 16)]
values = [100,150,120,180,200,170,220,250,240,260,230,300]

duration = 6

# =========================
# CHART ANIMATION
# =========================
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
        ax.text(v+2, i, f"£{int(v)}", color='white', va='center')

    plt.tight_layout()

    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    plt.close(fig)

    return image

chart = VideoClip(make_frame, duration=duration)

# =========================
# LEFT SIDE (MONEY)
# =========================
five = ImageClip("five.png").set_duration(duration).resize(height=120).set_position((40,150))
ten  = ImageClip("ten.png").set_duration(duration).resize(height=120).set_position((60,260))
twenty = ImageClip("twenty.png").set_duration(duration).resize(height=120).set_position((50,370))

# =========================
# RIGHT SIDE (PRIZES PANEL)
# =========================
def make_panel():
    fig, ax = plt.subplots(figsize=(4,6))
    fig.patch.set_facecolor('#0b3d91')
    ax.set_facecolor('#0b3d91')
    ax.axis('off')

    ax.text(0.1,0.8,"🥇 1st: Ninja Warriors",color='gold',fontsize=16,transform=ax.transAxes)
    ax.text(0.1,0.6,"🥈 2nd: Tenpin",color='silver',fontsize=16,transform=ax.transAxes)
    ax.text(0.1,0.4,"🥉 3rd: Soft Play",color='#cd7f32',fontsize=16,transform=ax.transAxes)

    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    plt.close(fig)
    return image

panel_img = make_panel()
panel = ImageClip(panel_img).set_duration(duration).set_position(("right","center"))

# Logos
ninja = ImageClip("ninja.png").set_duration(duration).resize(height=60).set_position((800,120))
tenpin = ImageClip("tenpin.png").set_duration(duration).resize(height=60).set_position((800,220))

# =========================
# COMBINE VIDEO
# =========================
video = CompositeVideoClip([
    chart,
    five, ten, twenty,
    panel,
    ninja, tenpin
])

# =========================
# AUDIO
# =========================
audio = AudioFileClip("drumroll.mp3").subclip(0, duration)
video = video.set_audio(audio)

# =========================
# EXPORT
# =========================
video.write_videofile("final_slide.mp4", fps=24)import numpy as np
import matplotlib.pyplot as plt
import requests
from moviepy.editor import VideoClip, AudioFileClip, ImageClip, CompositeVideoClip

# =========================
# AUTO DOWNLOAD FILES
# =========================
def download(url, filename):
    r = requests.get(url)
    with open(filename, "wb") as f:
        f.write(r.content)

# Logos + money + sound
download("https://www.kindpng.com/picc/m/83-832850_american-ninja-warrior-logo-png-american-ninja-warrior.png", "ninja.png")
download("https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Bowling_pins_icon.svg/512px-Bowling_pins_icon.svg.png", "tenpin.png")

download("https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Bank_of_England_%C2%A35_note.jpg/512px-Bank_of_England_%C2%A35_note.jpg", "five.png")
download("https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Bank_of_England_%C2%A310_note.jpg/512px-Bank_of_England_%C2%A310_note.jpg", "ten.png")
download("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Bank_of_England_%C2%A320_note.jpg/512px-Bank_of_England_%C2%A320_note.jpg", "twenty.png")

download("https://www.soundjay.com/misc/sounds/drum-roll-1.mp3", "drumroll.mp3")

# =========================
# DATA (EDIT VALUES ONLY)
# =========================
classes = [f"Class {i}" for i in range(4, 16)]
values = [100,150,120,180,200,170,220,250,240,260,230,300]

duration = 6

# =========================
# CHART ANIMATION
# =========================
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
        ax.text(v+2, i, f"£{int(v)}", color='white', va='center')

    plt.tight_layout()

    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    plt.close(fig)

    return image

chart = VideoClip(make_frame, duration=duration)

# =========================
# LEFT SIDE (MONEY)
# =========================
five = ImageClip("five.png").set_duration(duration).resize(height=120).set_position((40,150))
ten  = ImageClip("ten.png").set_duration(duration).resize(height=120).set_position((60,260))
twenty = ImageClip("twenty.png").set_duration(duration).resize(height=120).set_position((50,370))

# =========================
# RIGHT SIDE (PRIZES PANEL)
# =========================
def make_panel():
    fig, ax = plt.subplots(figsize=(4,6))
    fig.patch.set_facecolor('#0b3d91')
    ax.set_facecolor('#0b3d91')
    ax.axis('off')

    ax.text(0.1,0.8,"🥇 1st: Ninja Warriors",color='gold',fontsize=16,transform=ax.transAxes)
    ax.text(0.1,0.6,"🥈 2nd: Tenpin",color='silver',fontsize=16,transform=ax.transAxes)
    ax.text(0.1,0.4,"🥉 3rd: Soft Play",color='#cd7f32',fontsize=16,transform=ax.transAxes)

    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    plt.close(fig)
    return image

panel_img = make_panel()
panel = ImageClip(panel_img).set_duration(duration).set_position(("right","center"))

# Logos
ninja = ImageClip("ninja.png").set_duration(duration).resize(height=60).set_position((800,120))
tenpin = ImageClip("tenpin.png").set_duration(duration).resize(height=60).set_position((800,220))

# =========================
# COMBINE VIDEO
# =========================
video = CompositeVideoClip([
    chart,
    five, ten, twenty,
    panel,
    ninja, tenpin
])

# =========================
# AUDIO
# =========================
audio = AudioFileClip("drumroll.mp3").subclip(0, duration)
video = video.set_audio(audio)

# =========================
# EXPORT
# =========================
video.write_videofile("final_slide.mp4", fps=24)import numpy as np
import matplotlib.pyplot as plt
import requests
from moviepy.editor import VideoClip, AudioFileClip, ImageClip, CompositeVideoClip

# =========================
# AUTO DOWNLOAD FILES
# =========================
def download(url, filename):
    r = requests.get(url)
    with open(filename, "wb") as f:
        f.write(r.content)

# Logos + money + sound
download("https://www.kindpng.com/picc/m/83-832850_american-ninja-warrior-logo-png-american-ninja-warrior.png", "ninja.png")
download("https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Bowling_pins_icon.svg/512px-Bowling_pins_icon.svg.png", "tenpin.png")

download("https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Bank_of_England_%C2%A35_note.jpg/512px-Bank_of_England_%C2%A35_note.jpg", "five.png")
download("https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Bank_of_England_%C2%A310_note.jpg/512px-Bank_of_England_%C2%A310_note.jpg", "ten.png")
download("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Bank_of_England_%C2%A320_note.jpg/512px-Bank_of_England_%C2%A320_note.jpg", "twenty.png")

download("https://www.soundjay.com/misc/sounds/drum-roll-1.mp3", "drumroll.mp3")

# =========================
# DATA (EDIT VALUES ONLY)
# =========================
classes = [f"Class {i}" for i in range(4, 16)]
values = [100,150,120,180,200,170,220,250,240,260,230,300]

duration = 6

# =========================
# CHART ANIMATION
# =========================
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
        ax.text(v+2, i, f"£{int(v)}", color='white', va='center')

    plt.tight_layout()

    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    plt.close(fig)

    return image

chart = VideoClip(make_frame, duration=duration)

# =========================
# LEFT SIDE (MONEY)
# =========================
five = ImageClip("five.png").set_duration(duration).resize(height=120).set_position((40,150))
ten  = ImageClip("ten.png").set_duration(duration).resize(height=120).set_position((60,260))
twenty = ImageClip("twenty.png").set_duration(duration).resize(height=120).set_position((50,370))

# =========================
# RIGHT SIDE (PRIZES PANEL)
# =========================
def make_panel():
    fig, ax = plt.subplots(figsize=(4,6))
    fig.patch.set_facecolor('#0b3d91')
    ax.set_facecolor('#0b3d91')
    ax.axis('off')

    ax.text(0.1,0.8,"🥇 1st: Ninja Warriors",color='gold',fontsize=16,transform=ax.transAxes)
    ax.text(0.1,0.6,"🥈 2nd: Tenpin",color='silver',fontsize=16,transform=ax.transAxes)
    ax.text(0.1,0.4,"🥉 3rd: Soft Play",color='#cd7f32',fontsize=16,transform=ax.transAxes)

    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    plt.close(fig)
    return image

panel_img = make_panel()
panel = ImageClip(panel_img).set_duration(duration).set_position(("right","center"))

# Logos
ninja = ImageClip("ninja.png").set_duration(duration).resize(height=60).set_position((800,120))
tenpin = ImageClip("tenpin.png").set_duration(duration).resize(height=60).set_position((800,220))

# =========================
# COMBINE VIDEO
# =========================
video = CompositeVideoClip([
    chart,
    five, ten, twenty,
    panel,
    ninja, tenpin
])

# =========================
# AUDIO
# =========================
audio = AudioFileClip("drumroll.mp3").subclip(0, duration)
video = video.set_audio(audio)

# =========================
# EXPORT
# =========================
video.write_videofile("final_slide.mp4", fps=24)
