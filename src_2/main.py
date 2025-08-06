# Create an interactive OpenCV-based tool using OOP to:
# 1. Calibrate image scale (pixels to mm) by clicking two points and entering known distance.
# 2. Adjust image using trackbars (blur, alpha, beta).
# 3. Measure distance between any two clicked points using calibrated scale.

import cv2
import numpy as np

class KeyImageCalibrator:
    def __init__(self, image_path):
        self.original = cv2.imread(image_path)
        if self.original is None:
            raise FileNotFoundError("Image not found.")

        self.original = cv2.resize(self.original, (800, 400))
        self.image = self.original.copy()
        self.clone = self.original.copy()
        self.alpha = 1.0
        self.beta = 0
        self.blur_val = 1
        self.scale = None  # pixels per mm
        self.points = []
        self.last_measure_text = ""
        self.last_measure_pos = (0, 0)


        self.setup_ui()

    def setup_ui(self):
        cv2.namedWindow('Calibrator')
        cv2.setMouseCallback('Calibrator', self.mouse_callback)
        cv2.createTrackbar('Blur', 'Calibrator', 1, 50, self.update_blur)
        cv2.createTrackbar('Alpha x0.1', 'Calibrator', 10, 30, self.update_alpha)
        cv2.createTrackbar('Beta', 'Calibrator', 0, 100, self.update_beta)

    def update_blur(self, val):
        self.blur_val = val if val % 2 == 1 else val + 1
        self.apply_filters()

    def update_alpha(self, val):
        self.alpha = val / 10.0
        self.apply_filters()

    def update_beta(self, val):
        self.beta = val
        self.apply_filters()

    def apply_filters(self):
        img = cv2.convertScaleAbs(self.original, alpha=self.alpha, beta=self.beta)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (max(1, self.blur_val), max(1, self.blur_val)), 0)
        self.image = cv2.cvtColor(blur, cv2.COLOR_GRAY2BGR)
        self.clone = self.image.copy()
        self.redraw_points()

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.points.append((x, y))
            if len(self.points) == 2 and self.scale is None:
                # Prompt for known distance
                print("Enter real distance in mm between the two points:")
                self.draw_text("Enter value in terminal", (10, 20))
            elif len(self.points) == 4 and self.scale:
                # Measure another segment
                p1, p2 = self.points[2], self.points[3]
                pixel_dist = np.linalg.norm(np.array(p1) - np.array(p2))
                mm_dist = pixel_dist / self.scale
                print(f"Measured distance: {mm_dist:.2f} mm")
                self.last_measure_text = f"{mm_dist:.2f} mm"
                self.last_measure_pos = p2


            self.redraw_points()


    def draw_text(self, text, pos):
        cv2.putText(self.image, text, pos, cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    def redraw_points(self):
        self.image = self.clone.copy()
        for pt in self.points:
            cv2.circle(self.image, pt, 5, (0, 0, 255), -1)
        if len(self.points) >= 2:
            cv2.line(self.image, self.points[0], self.points[1], (255, 0, 0), 2)
        if len(self.points) == 4:
            cv2.line(self.image, self.points[2], self.points[3], (0, 255, 255), 2)
        if self.last_measure_text:
            self.draw_text(self.last_measure_text, self.last_measure_pos)


    def run(self):
        while True:
            cv2.imshow("Calibrator", self.image)
            key = cv2.waitKey(10) & 0xFF

            if key == ord('q') or key == 27:
                break
            elif key == ord('r'):
                self.points = []
                self.scale = None
                self.apply_filters()
            elif key == ord('s') and len(self.points) == 2 and self.scale is None:
                # Input known real distance in mm
                try:
                    known_mm = float(input("Enter real distance in mm: "))
                    pixel_dist = np.linalg.norm(np.array(self.points[0]) - np.array(self.points[1]))
                    self.scale = pixel_dist / known_mm
                    print(f"Calibration complete: {self.scale:.2f} pixels/mm")
                except:
                    print("Invalid input. Try again.")

        cv2.destroyAllWindows()

# Example usage
calibrator = KeyImageCalibrator("sample_0.png")
calibrator.run()

