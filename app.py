import cv2
import os
import numpy as np
from PIL import Image, ImageDraw, ImageSequence

files = input("Enter folder name: ")
rows = int(input("Enter rows quantity: "))
cols = int(input("Enter cols quantity: "))
frame_duration = int(input("Enter frame duration: "))
generateFinal = input("Generate Final (Y/N)? ")
print()

os.makedirs("gif", exist_ok=True)
os.makedirs("mp4", exist_ok=True)
os.makedirs("cutted", exist_ok=True)

all_frames = []
finalName = ""

frame_files = sorted([f for f in os.listdir(files) if f.endswith(".png")])

for image in frame_files:
    name = os.path.splitext(image)[0]
    print(f"Processing {image}...")

    sprite_sheet_path = os.path.join(files, image)
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

    all_frames.extend(frames)  

    gif_path = os.path.join("gif", f"{name}.gif")
    frames[0].save(gif_path, save_all=True, append_images=frames[1:], optimize=False, duration=frame_duration, loop=0)
    print("GIF:", gif_path)

    draw = ImageDraw.Draw(sprite_sheet)
    for row in range(1, rows):
        y = row * frame_height
        draw.line([(0, y), (sprite_sheet.width, y)], fill="red", width=1)
    for col in range(1, cols):
        x = col * frame_width
        draw.line([(x, 0), (x, sprite_sheet.height)], fill="red", width=1)

    grid_image_path = os.path.join("cutted", f"{name}.png")
    sprite_sheet.save(grid_image_path)
    finalName += name + "-"
    print("CUTTED:", grid_image_path)
    print(f"-----FILE {name} FINISHED-----\n")

if all_frames and generateFinal.lower() == "y":
    unified_gif = f"gif/{finalName}.gif"
    unified_mp4 = f"mp4/{finalName}.mp4"

    print(f"Processing Final GIF...")
    all_frames[0].save(unified_gif, save_all=True, append_images=all_frames[1:], optimize=False, duration=frame_duration, loop=0)
    print("Unified GIF:", unified_gif)

    print(f"Processing Final MP4...")
    width, height = all_frames[0].size
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(unified_mp4, fourcc, 1000 // frame_duration, (width, height))

    for frame in all_frames:
        frame_cv = cv2.cvtColor(np.array(frame.convert("RGB")), cv2.COLOR_RGB2BGR)
        video.write(frame_cv)

    video.release()
    print("Unified MP4:", unified_mp4)
print(f"-----PROCESS FINISHED-----")
