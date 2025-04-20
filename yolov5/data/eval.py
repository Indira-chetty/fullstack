
import json
import os
import cv2
import easyocr
from jiwer import cer, wer
from Levenshtein import distance as levenshtein_distance

# Load COCO-Text dataset annotations
with open("C://Users//INDIRA//Downloads//WeSee-main//WeSee-main//yolov5//data//cocotext.v2.json", "r") as f:
    coco_text = json.load(f)

# Get valid images with annotations
valid_images = list(coco_text["anns"].keys())[:10]  # Get first 10 valid images
image_id = valid_images[0]  # Select first valid image

# Locate the image file
image_dirs = ["cocotext.v2/train_images/", "cocotext.v2/val_images/", "cocotext.v2/test_images/"]
image_path = None

for folder in image_dirs:
    possible_path = os.path.join(folder, f"COCO_train2014_{image_id.zfill(12)}.jpg")
    if os.path.exists(possible_path):
        image_path = possible_path
        break

if not image_path:
    print(f"❌ Image not found for {image_id}. Try another image ID.")
    exit()

# Initialize OCR model
reader = easyocr.Reader(['en'])

# Load image and perform OCR
image = cv2.imread(image_path)
ocr_result = reader.readtext(image, detail=0)  # Extract only text
ocr_text = " ".join(ocr_result)

# Get ground truth text from annotations
true_text = coco_text["anns"][image_id]["utf8_string"] if image_id in coco_text["anns"] else "N/A"

# Compute OCR Evaluation Metrics
cer_score = cer(true_text.lower(), ocr_text.lower()) if true_text != "N/A" else None
wer_score = wer(true_text.lower(), ocr_text.lower()) if true_text != "N/A" else None
lev_dist = levenshtein_distance(true_text.lower(), ocr_text.lower()) if true_text != "N/A" else None

# Compute IoU for Bounding Box Evaluation
def calculate_iou(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    intersection = max(0, xB - xA) * max(0, yB - yA)
    boxA_area = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    boxB_area = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
    return intersection / float(boxA_area + boxB_area - intersection)

gt_box = coco_text["anns"][image_id]["bbox"] if image_id in coco_text["anns"] else None
if gt_box:
    gt_box = [gt_box[0], gt_box[1], gt_box[0] + gt_box[2], gt_box[1] + gt_box[3]]  # Convert to [x1, y1, x2, y2]
    pred_box = [50, 30, 200, 150]  # Replace with actual detected bounding box
    iou_score = calculate_iou(gt_box, pred_box)
else:
    iou_score = None

# Display results
evaluation_results = {
    "Image ID": image_id,
    "OCR Output": ocr_text,
    "Ground Truth": true_text,
    "CER": cer_score,
    "WER": wer_score,
    "Levenshtein Distance": lev_dist,
    "IoU Score": iou_score
}

# Print Evaluation Summary
print("\n📊 OCR Model Evaluation Results:")
for key, value in evaluation_results.items():
    print(f"✅ {key}: {value}")
