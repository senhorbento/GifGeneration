import cv2
import os
import numpy as np
from PIL import Image, ImageDraw, ImageSequence

image = input("Enter file name: ")

# Load the sprite sheet
sprite_sheet_path = "frames/"+image+".png"
sprite_sheet = Image.open(sprite_sheet_path)

# Define the number of rows and columns
rows, cols = 3, 3

# Calculate width and height of each frame
frame_width = sprite_sheet.width // cols
frame_height = sprite_sheet.height // rows
print(frame_width,"x",frame_height)

# Extract frames
frames = []
for row in range(rows):
    for col in range(cols):
        left = col * frame_width
        upper = row * frame_height
        right = left + frame_width
        lower = upper + frame_height
        frame = sprite_sheet.crop((left, upper, right, lower))
        frames.append(frame)

# Save as GIF
gif_path = "gif/"+image+".gif"
frames[0].save(gif_path, save_all=True, append_images=frames[1:], optimize=False, duration=100, loop=0)

print("GIF:", gif_path)

draw = ImageDraw.Draw(sprite_sheet)

for row in range(1, rows):
    y = row * frame_height
    draw.line([(0, y), (sprite_sheet.width, y)], fill="red", width=1)

# Draw vertical lines
for col in range(1, cols):
    x = col * frame_width
    draw.line([(x, 0), (x, sprite_sheet.height)], fill="red", width=1)

# Save the image with grid lines
grid_image_path = "cutted/"+image+".png"
sprite_sheet.save(grid_image_path)

print("CUTTED:", grid_image_path)

mp4_path = "mp4/" + image + ".mp4"
# Load the GIF
gif = Image.open(gif_path)
frames = [frame.copy().convert('RGB') for frame in ImageSequence.Iterator(gif)]
width, height = frames[0].size

# Define video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter(mp4_path, fourcc, 10, (width, height))  # 10 FPS

# Write each frame
for frame in frames:
    frame_cv = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
    video.write(frame_cv)

video.release()
print("MP4:", mp4_path)