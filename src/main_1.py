import cv2
import numpy as np

# Load image
img = cv2.imread('sample_0.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blur, 50, 150)

# Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Get largest contour (assume it's the key)
key_contour = max(contours, key=cv2.contourArea)

# Draw the key contour (only outline)
contour_img = img.copy()
cv2.drawContours(contour_img, [key_contour], -1, (0, 255, 0), 2)

# Save the result
cv2.imwrite("key_contour_output.jpg", contour_img)
print("✅ Key contour saved as 'key_contour_output.jpg'")
