import os
from PIL import Image, ImageChops, ImageDraw

def compare_images(baseline_path, new_path, diff_path, threshold=30):
    if not os.path.exists(baseline_path) or not os.path.exists(new_path):
        print(f"❌ Baseline or new screenshot not found.")
        return False

    baseline = Image.open(baseline_path).convert('RGB')
    new = Image.open(new_path).convert('RGB')

    if baseline.size != new.size:
        print(f"⚠️ Image size mismatch: {baseline.size} vs {new.size}")
        return False

    diff = ImageChops.difference(baseline, new)
    
    if not diff.getbbox():
        print("✅ Images are identical.")
        return True

    pixels = diff.getdata()
    changed_pixels = sum(1 for pixel in pixels if sum(pixel) > threshold)
    total_pixels = len(pixels)
    percent_diff = (changed_pixels / total_pixels) * 100

    print(f"🔍 Visual difference: {percent_diff:.2f}%")

    if percent_diff > 1.0: 
        print(f"❌ Change detected ({percent_diff:.2f}%) — Saving diff image.")
        highlight_diff_image(baseline, new, diff_path, diff)
        return False

    return True

def highlight_diff_image(baseline, new, diff_path, diff):
    highlighted = new.copy()
    draw = ImageDraw.Draw(highlighted)

    for x in range(diff.width):
        for y in range(diff.height):
            r, g, b = diff.getpixel((x, y))
            if r + g + b > 30:
                draw.rectangle([x, y, x + 1, y + 1], fill="red")

    os.makedirs(os.path.dirname(diff_path), exist_ok=True)
    highlighted.save(diff_path)
    print(f"🖼️ Diff image saved: {diff_path}")
