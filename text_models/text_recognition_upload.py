import cv2
import easyocr
from gtts import gTTS
import os
from datetime import datetime
from flask import Flask, render_template, request, Response

app = Flask(__name__)

# Set upload directories for images and audio
app.config['UPLOAD_FOLDER'] = 'static/captured'
app.config['AUDIO_FOLDER'] = 'static/audio'

# Initialize EasyOCR Reader
reader = easyocr.Reader(['en'])  # English OCR

def perform_ocr_and_audio(image_path):
    """Process image: enhance contrast, perform OCR, and convert text to speech."""
    
    # Load the image
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    def adjust_brightness_contrast(image, alpha=1.5, beta=20):
        """Enhance brightness and contrast for better OCR performance."""
        return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

    # Adjust image contrast/brightness
    img_adjusted = adjust_brightness_contrast(img)

    # Save the adjusted image
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    adjusted_image_path = os.path.join(app.config['UPLOAD_FOLDER'], f'adjusted_image_{timestamp}.jpg')
    cv2.imwrite(adjusted_image_path, cv2.cvtColor(img_adjusted, cv2.COLOR_RGB2BGR))

    # Perform OCR using EasyOCR
    results = reader.readtext(img_adjusted)
    extracted_text = " ".join([result[1] for result in results])  # Extract detected text

    # Print extracted text
    print(extracted_text)

    if extracted_text.strip():  # Proceed only if text is detected
        # Convert text to speech
        tts = gTTS(text=extracted_text, lang='en')

        # Save the audio file
        os.makedirs(app.config['AUDIO_FOLDER'], exist_ok=True)
        audio_file = os.path.join(app.config['AUDIO_FOLDER'], f'output_{timestamp}.mp3')
        tts.save(audio_file)

        return extracted_text, audio_file, adjusted_image_path, timestamp

    return "No text detected", "", adjusted_image_path, timestamp

# Flask route for file upload & OCR processing
@app.route("/", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if 'file' not in request.files:
            return "No file uploaded", 400

        file = request.files["file"]
        if file.filename == "":
            return "No selected file", 400

        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            text, audio_file, processed_image, timestamp = perform_ocr_and_audio(file_path)
    
