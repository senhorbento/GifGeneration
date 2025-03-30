import cv2
import os
import numpy as np
from PIL import Image, ImageDraw, ImageSequence

# Create folders if they don't exist
os.makedirs("gif", exist_ok=True)
os.makedirs("mp4", exist_ok=True)
os.makedirs("cutted", exist_ok=True)

# Config
rows, cols = 3, 3
frame_duration = 150  # ms per frame
folder = input("Enter folder name: ")
files = "/multiple/" + folder

origin_path = "frames" + files

os.makedirs("gif" + files, exist_ok=True)
os.makedirs("cutted" + files, exist_ok=True)
os.makedirs("mp4" + files, exist_ok=True)

unified_gif = "gif" + files + "/final.gif"
unified_mp4 = "mp4" + files + "/final.mp4"

# Collect all processed frames
all_frames = []

# Get all PNG files from the frames folder
frame_files = sorted([f for f in os.listdir(origin_path) if f.endswith(".png")])

for image in frame_files:
    name = os.path.splitext(image)[0]
    print(f"Processing {image}...")

    sprite_sheet_path = os.path.join(origin_path, image)
    sprite_sheet = Image.open(sprite_sheet_path)

    frame_width = sprite_sheet.width // cols
    frame_height = sprite_sheet.height // rows
    print(f"{frame_width} x {frame_height}")

    frames = []
    for row in range(rows):
        for col in range(cols):
            left = col * frame_width
            upper = row * frame_height
            right = left + frame_width
            lower = upper + frame_height
            frame = sprite_sheet.crop((left, upper, right, lower))
            frames.append(frame)

    all_frames.extend(frames)  # Add to final animation

    # Save individual GIF (optional)
    gif_path = os.path.join("gif" + files, f"{name}.gif")
    frames[0].save(gif_path, save_all=True, append_images=frames[1:], optimize=False, duration=frame_duration, loop=0)
    print("GIF:", gif_path)

    # Draw grid lines
    draw = ImageDraw.Draw(sprite_sheet)
    for row in range(1, rows):
        y = row * frame_height
        draw.line([(0, y), (sprite_sheet.width, y)], fill="red", width=1)
    for col in range(1, cols):
        x = col * frame_width
        draw.line([(x, 0), (x, sprite_sheet.height)], fill="red", width=1)

    # Save image with grid lines
    grid_image_path = os.path.join("cutted" + files, f"{name}.png")
    sprite_sheet.save(grid_image_path)
    print("CUTTED:", grid_image_path)
    print(f"-----FILE {name} FINISHED-----\n")

# Save unified GIF
if all_frames:
    all_frames[0].save(unified_gif, save_all=True, append_images=all_frames[1:], optimize=False, duration=frame_duration, loop=0)
    print("Unified GIF:", unified_gif)

    # Save unified MP4
    width, height = all_frames[0].size
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(unified_mp4, fourcc, 1000 // frame_duration, (width, height))

    for frame in all_frames:
        frame_cv = cv2.cvtColor(np.array(frame.convert("RGB")), cv2.COLOR_RGB2BGR)
        video.write(frame_cv)

    video.release()
    print("Unified MP4:", unified_mp4)
else:
    print("No frames found!")
