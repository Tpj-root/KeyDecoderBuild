import cv2
import numpy as np

# Load image
img = cv2.imread('sample_0.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blur, 50, 150)

# Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Assume biggest contour is the key
key_contour = max(contours, key=cv2.contourArea)
x, y, w, h = cv2.boundingRect(key_contour)

# Draw bounding box
key_img = img.copy()
cv2.rectangle(key_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
cv2.imshow("Key Detected", key_img)
cv2.waitKey(0)

# === Calibration ===
known_length_mm = 60.0  # Change this to real key length in mm
pixels_per_mm = w / known_length_mm
print(f"Pixels per mm: {pixels_per_mm:.2f}")

# You can now use pixels_per_mm to convert cut depths
