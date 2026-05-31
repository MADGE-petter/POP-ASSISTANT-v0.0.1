#!/usr/bin/env python3
"""
Create a simple icon for Pop Assistant
"""

from PIL import Image, ImageDraw

# Create 256x256 icon
size = 256
img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Draw gradient circle (green-blue like hologram theme)
for i in range(size//2, 0, -1):
    # Gradient from center
    ratio = i / (size//2)
    r = int(0 + (0 - 0) * ratio)  # 0
    g = int(255 + (100 - 255) * ratio)  # 255 to 100
    b = int(136 + (200 - 136) * ratio)  # 136 to 200
    alpha = int(255 * (1 - ratio * 0.5))
    
    x = size//2 - i
    y = size//2 - i
    draw.ellipse([x, y, x + i*2, y + i*2], fill=(r, g, b, alpha))

# Draw inner white circle for "bot face"
face_size = size // 3
dx = (size - face_size) // 2
dy = (size - face_size) // 2
draw.ellipse([dx, dy, dx + face_size, dy + face_size], fill=(255, 255, 255, 230))

# Draw eyes
eye_size = face_size // 5
eye_y = dy + face_size // 3
left_eye_x = dx + face_size // 4
right_eye_x = dx + face_size * 3 // 4

draw.ellipse([left_eye_x - eye_size//2, eye_y - eye_size//2, 
              left_eye_x + eye_size//2, eye_y + eye_size//2], fill=(0, 0, 0))
draw.ellipse([right_eye_x - eye_size//2, eye_y - eye_size//2, 
              right_eye_x + eye_size//2, eye_y + eye_size//2], fill=(0, 0, 0))

# Draw smile (simple arc)
smile_y = dy + face_size * 2 // 3
smile_width = face_size // 2
smile_left = dx + face_size // 4
for i in range(smile_width):
    x = smile_left + i
    y = smile_y + abs(i - smile_width//2) // 4
    draw.ellipse([x-2, y-2, x+2, y+2], fill=(0, 0, 0))

img.save('icon.png')
print("Created icon.png (256x256)")
# Save as ICO for Windows with multiple sizes for better compatibility
sizes = [(16,16), (24,24), (32,32), (48,48), (64,64), (96,96), (128,128), (256,256)]
img.save('icon.ico', format='ICO', sizes=sizes)
print(f"Created icon.ico with {len(sizes)} sizes: {sizes}")
