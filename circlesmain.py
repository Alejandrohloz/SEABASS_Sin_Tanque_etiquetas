import cv2
import numpy as np

class CircleDetector:
    def __init__(self, min_radius=30, max_radius=400):
        self.min_radius = min_radius
        self.max_radius = max_radius
    
    def process_frame(self, frame):
        # Convierte el fotograma a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Aplica un desenfoque para reducir ruido
        gray_blurred = cv2.blur(gray, (3, 3))

        # Aplica la transformada de Hough para detectar círculos
        detected_circles = cv2.HoughCircles(
            gray_blurred,
            cv2.HOUGH_GRADIENT,
            1,
            20,
            param1=50,
            param2=30,
            minRadius=self.min_radius,
            maxRadius=self.max_radius
        )

        # Si se detectan círculos, dibújalos
        if detected_circles is not None:
            # Convierte los parámetros de los círculos (a, b, r) a enteros
            detected_circles = np.uint16(np.around(detected_circles))

            # Dibuja los círculos detectados
            for pt in detected_circles[0, :]:
                a, b, r = pt[0], pt[1], pt[2]

                # Dibuja la circunferencia del círculo
                cv2.circle(frame, (a, b), r, (0, 255, 0), 2)

                # Dibuja un pequeño círculo (de radio 1) para mostrar el centro
                cv2.circle(frame, (a, b), 1, (0, 0, 255), 3)

        return frame