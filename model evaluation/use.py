from PIL import Image, ImageDraw, ImageFont

# Function to create OCR test images
def create_ocr_image(text, filename):
    img = Image.new('RGB', (400, 100), color=(255, 255, 255))  # White background
    draw = ImageDraw.Draw(img)

    # Try loading a font
    try:
        font = ImageFont.truetype("arial.ttf", 24)  # Use Arial font if available
    except IOError:
        font = ImageFont.load_default()  # Use default font if Arial is unavailable

    draw.text((10, 40), text, fill=(0, 0, 0), font=font)  # Black text
    img.save(filename)
    print(f"Image saved: {filename}")

# Generate three images
create_ocr_image("The quick brown fox", "image1.jpg")
create_ocr_image("Machine learning is amazing", "image2.jpg")
create_ocr_image("Deep learning for OCR", "image3.jpg")
