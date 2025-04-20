import easyocr
import cv2
import numpy as np
from jiwer import wer, cer
from difflib import SequenceMatcher
from Levenshtein import distance as levenshtein_distance

# Initialize EasyOCR model
reader = easyocr.Reader(['en'])  # Supports multiple languages

# Load Ground Truth Data (Image + Expected Text)
ground_truth = {
    "C://Users//INDIRA//Downloads//WeSee-main//WeSee-main//image1.jpg": "The quick brown fox",
    "C://Users//INDIRA//Downloads//WeSee-main//WeSee-main//image2.jpg": "Machine learning is amazing",
    "C://Users//INDIRA//Downloads//WeSee-main//WeSee-main//image3.jpg": "Deep learning for OCR"
}

def evaluate_ocr(image_path, true_text):
    """Evaluates OCR model using CER, WER, and Levenshtein Distance"""
    
    # Read image
    image = cv2.imread(image_path)
    
    # Perform OCR using EasyOCR
    result = reader.readtext(image, detail=0)
    
    # Join extracted text (OCR output)
    ocr_text = " ".join(result)

    # Compute Evaluation Metrics
    cer_score = cer(true_text.lower(), ocr_text.lower())
    wer_score = wer(true_text.lower(), ocr_text.lower())
    lev_dist = levenshtein_distance(true_text.lower(), ocr_text.lower())

    # Print results
    print(f"🔹 Image: {image_path}")
    print(f"✅ Ground Truth: {true_text}")
    print(f"🔍 OCR Output: {ocr_text}")
    print(f"📌 CER: {cer_score:.4f} | WER: {wer_score:.4f} | Levenshtein Distance: {lev_dist}\n")

# Evaluate OCR for all test images
for img, true_text in ground_truth.items():
    evaluate_ocr(img, true_text)

def calculate_iou(boxA, boxB):
    """Computes IoU (Intersection over Union) between two bounding boxes"""
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    # Compute the intersection area
    intersection = max(0, xB - xA) * max(0, yB - yA)

    # Compute the area of both bounding boxes
    boxA_area = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    boxB_area = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])

    # Compute IoU
    iou = intersection / float(boxA_area + boxB_area - intersection)
    return iou

# Example Ground Truth & Predicted Bounding Box
gt_box = [50, 30, 200, 150]  # [x1, y1, x2, y2]
pred_box = [55, 35, 190, 140]

iou_score = calculate_iou(gt_box, pred_box)
print(f"📌 IoU Score: {iou_score:.4f}")
