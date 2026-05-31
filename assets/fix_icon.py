#!/usr/bin/env python3
"""Create proper Windows ICO file"""
from PIL import Image, ImageDraw

size = 256
img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Draw gradient circle
cx, cy = size // 2, size // 2
for i in range(size // 2, 0, -1):
    ratio = i / (size // 2)
    r = int(0 * (1 - ratio) + 50 * ratio)
    g = int(255 * (1 - ratio) + 100 * ratio)
    b = int(136 * (1 - ratio) + 200 * ratio)
    alpha = int(255 * (1 - ratio * 0.3))
    
    x1 = cx - i
    y1 = cy - i
    x2 = cx + i
    y2 = cy + i
    draw.ellipse([x1, y1, x2, y2], fill=(r, g, b, alpha))

# Draw white face circle
face_size = size // 2
fx = (size - face_size) // 2
fy = (size - face_size) // 2
draw.ellipse([fx, fy, fx + face_size, fy + face_size], fill=(255, 255, 255, 240))

# Draw eyes
eye_size = face_size // 6
eye_y = fy + face_size // 3
left_eye_x = fx + face_size // 3
right_eye_x = fx + face_size * 2 // 3

draw.ellipse([left_eye_x - eye_size//2, eye_y - eye_size//2,
              left_eye_x + eye_size//2, eye_y + eye_size//2], fill=(0, 50, 100))
draw.ellipse([right_eye_x - eye_size//2, eye_y - eye_size//2,
              right_eye_x + eye_size//2, eye_y + eye_size//2], fill=(0, 50, 100))

# Draw smile
smile_y = fy + face_size * 2 // 3
smile_width = face_size // 2
smile_left = fx + face_size // 4
for i in range(smile_width):
    x = smile_left + i
    y_offset = abs(i - smile_width//2) // 3
    y = smile_y + y_offset
    draw.ellipse([x-3, y-3, x+3, y+3], fill=(0, 50, 100))

# Save as PNG
img.save('icon.png')
print("Created icon.png")

# Create ICO with multiple sizes
ico_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (96, 96), (128, 128), (256, 256)]
images = []
for w, h in ico_sizes:
    img_resized = img.resize((w, h), Image.LANCZOS)
    # Convert to RGB with white background for ICO compatibility
    if img_resized.mode == 'RGBA':
        rgb_img = Image.new('RGB', (w, h), (255, 255, 255))
        rgb_img.paste(img_resized, mask=img_resized.split()[3])
        images.append(rgb_img)
    else:
        images.append(img_resized)

# Save first image as base, append others
images[0].save('icon.ico', format='ICO', sizes=ico_sizes, append_images=images[1:])
print(f"Created icon.ico with {len(ico_sizes)} sizes")
print(f"Sizes: {ico_sizes}")
