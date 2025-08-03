import cv2
import numpy as np

# Load image
original = cv2.imread("sample_0.png")
if original is None:
    raise Exception("Image not found!")

# Resize (optional)
original = cv2.resize(original, (800, 400))

def nothing(x):
    pass

# Create window
cv2.namedWindow('Controls')

# Add trackbars
cv2.createTrackbar('Canny Thresh1', 'Controls', 50, 500, nothing)
cv2.createTrackbar('Canny Thresh2', 'Controls', 150, 500, nothing)
cv2.createTrackbar('Blur', 'Controls', 1, 50, nothing)
cv2.createTrackbar('Alpha x0.1', 'Controls', 10, 30, nothing)  # 1.0 to 3.0
cv2.createTrackbar('Beta', 'Controls', 0, 100, nothing)

while True:
    img = original.copy()

    # Read values
    t1 = cv2.getTrackbarPos('Canny Thresh1', 'Controls')
    t2 = cv2.getTrackbarPos('Canny Thresh2', 'Controls')
    blur_val = cv2.getTrackbarPos('Blur', 'Controls')
    alpha = cv2.getTrackbarPos('Alpha x0.1', 'Controls') / 10.0
    beta = cv2.getTrackbarPos('Beta', 'Controls')

    # Apply contrast and brightness
    img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply blur
    if blur_val % 2 == 0: blur_val += 1  # Ensure odd number
    if blur_val < 1: blur_val = 1
    blur = cv2.GaussianBlur(gray, (blur_val, blur_val), 0)

    # Apply Canny
    edges = cv2.Canny(blur, t1, t2)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        key_contour = max(contours, key=cv2.contourArea)
        cv2.drawContours(img, [key_contour], -1, (0, 255, 0), 2)

    # Stack images for view
    edge_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    combined = np.hstack((img, edge_bgr))
    cv2.imshow("Key Shape Viewer", combined)

    key = cv2.waitKey(10) & 0xFF
    if key == 27:  # ESC to exit
        break

cv2.destroyAllWindows()
