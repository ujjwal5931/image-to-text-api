from PIL import Image, ImageDraw, ImageFont
import os

# Create a new image with white background
img = Image.new('RGB', (400, 200), color=(255, 255, 255))
d = ImageDraw.Draw(img)

# Try to use a default font
try:
    # Try to use Arial font if available
    font = ImageFont.truetype("arial.ttf", 36)
except IOError:
    # Fallback to default font
    font = ImageFont.load_default()

# Add text to the image
d.text((50, 50), "Hello World!", fill=(0, 0, 0), font=font)
d.text((50, 100), "Testing OCR", fill=(0, 0, 0), font=font)

# Save the image
img.save('test_images/sample_text.png')

print(f"Test image created at: {os.path.abspath('test_images/sample_text.png')}") 