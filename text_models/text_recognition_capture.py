import cv2
import easyocr
from gtts import gTTS
import os
from datetime import datetime

# Initialize EasyOCR Reader
reader = easyocr.Reader(['en'])  # Supports multiple languages

def adjust_brightness_contrast(img, alpha=1.0, beta=0):
    """Adjust brightness and contrast of an image."""
    adjusted_img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
    return adjusted_img

def perform_text_capture():
    """Capture an image, process it, extract text using EasyOCR, and generate speech."""
    
    cap = cv2.VideoCapture(0)  # Open webcam

    while True:
        ret, frame = cap.read()
        cv2.imshow('Press "c" to Capture', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            # Save the original image
            os.makedirs('static/captured', exist_ok=True)  # Ensure directory exists
            original_img_path = 'static/captured/original_image.jpg'
            cv2.imwrite(original_img_path, frame)

            # Adjust brightness and contrast
            adjusted_frame = adjust_brightness_contrast(frame, alpha=1.5, beta=20)
            adjusted_img_path = 'static/captured/adjusted_image.jpg'
            cv2.imwrite(adjusted_img_path, adjusted_frame)

            cap.release()
            cv2.destroyAllWindows()
            print("Images captured and saved")

            break

        elif key == 27:  # Press 'Esc' to exit
            cap.release()
            cv2.destroyAllWindows()
            return "Process exited.", "", ""

    # Load the adjusted image for OCR
    if os.path.exists(adjusted_img_path):
        img = cv2.imread(adjusted_img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert for EasyOCR processing

        # Perform text recognition with EasyOCR
        result = reader.readtext(img, detail=0)  # Extract text only
        text_output = " ".join(result)  # Join recognized words

        print("Recognized text:")
        print(text_output)

        if text_output.strip():  # Check if any text is detected
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

            # Convert recognized text to speech using gTTS
            os.makedirs('static/audio', exist_ok=True)  # Ensure directory exists
            audio_path = f"static/audio/output_audio_{timestamp}.mp3"
            tts = gTTS(text=text_output, lang='en')
            tts.save(audio_path)

            return text_output, adjusted_img_path, audio_path, timestamp
        else:
            return "Error: No text detected in the captured image", "", ""

    else:
        return "Error: Adjusted image not found", "", ""

